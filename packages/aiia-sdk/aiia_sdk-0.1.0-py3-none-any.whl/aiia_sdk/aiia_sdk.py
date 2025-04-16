import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import tldextract


class AIIA:
    def __init__(self, api_key: str, client_secret: str, ia_id: str, endpoint: str = "http://localhost:5001"):
        self.api_key = api_key
        self.client_secret = client_secret.encode()
        self.ia_id = ia_id
        self.endpoint = endpoint.rstrip('/')
        self.cache_file = Path(__file__).parent / "cache" / "actions_cache.json"
        self._init_cache()

    def _init_cache(self) -> None:
        self.cache_file.parent.mkdir(exist_ok=True)
        if not self.cache_file.exists():
            self.cache_file.write_text("{}")

    def _load_cache(self) -> Dict[str, Any]:
        try:
            return json.loads(self.cache_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_cache(self, data: Dict[str, Any]) -> None:
        self.cache_file.write_text(json.dumps(data))

    def _get_action_definition(self, action_code: str) -> Dict[str, Any]:
        cache = self._load_cache()
        if action_code in cache:
            return cache[action_code]

        try:
            response = requests.get(
                f"{self.endpoint}/actions/{action_code}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            response.raise_for_status()
            action_data = response.json()
            cache[action_code] = action_data
            self._save_cache(cache)
            return action_data
        except requests.exceptions.RequestException:
            return {
                "code": action_code,
                "description": f"Acción {action_code}",
                "category": "general",
                "sensitive": False
            }

    def log_action(self, action_code: str, context: Optional[Dict[str, Any]] = None) -> bool:
        try:
            action_def = self._get_action_definition(action_code)
            timestamp = datetime.now(timezone.utc).isoformat()
            data_to_sign = f"{timestamp}:{action_code}:{self.ia_id}"
            signature = hmac.new(
                self.client_secret,
                data_to_sign.encode(),
                hashlib.sha256
            ).hexdigest()

            context = context or {}
            encrypted_context = {}
            public_context = {}

            for key, value in context.items():
                if action_def.get("sensitive", False):
                    encrypted_context[key] = self._encrypt_value(value)
                else:
                    public_context[key] = value

            domain = None
            for key, value in context.items():
                if "email" in key and isinstance(value, str) and "@" in value:
                    domain_candidate = value.split("@")[1].lower()
                    extracted = tldextract.extract(domain_candidate)
                    if extracted.domain and extracted.suffix:
                        domain = f"{extracted.domain}.{extracted.suffix}"
                    else:
                        domain = None
                    break

            log_payload = {
                "timestamp": timestamp,
                "action": action_code,
                "ia_id": self.ia_id,
                "signature": signature,
                "context_encrypted": encrypted_context,
                "context_public": public_context,
                "encryption_metadata": {
                    "algorithm": "AES-256-GCM",
                    "key_derivation": "SHA-256",
                    "key_owner": "client"
                },
                "domain": domain
            }

            response = requests.post(
                f"{self.endpoint}/receive_log",
                json=log_payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Error al registrar acción '{action_code}': {str(e)}")
            return False

    def validate_credentials(self) -> bool:
        try:
            response = requests.get(
                f"{self.endpoint}/validate_ia",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=3
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _encrypt_value(self, plaintext: str) -> str:
        key = hashlib.sha256(self.client_secret).digest()
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(str(plaintext).encode()) + encryptor.finalize()
        return "aes256:" + base64.b64encode(nonce + encryptor.tag + ciphertext).decode()