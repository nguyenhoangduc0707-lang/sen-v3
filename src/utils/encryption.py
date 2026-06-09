"""
Encryption utilities for sensitive data (tokens, cookies, app secrets).
Uses Fernet (symmetric encryption from cryptography).
"""

from cryptography.fernet import Fernet
import logging
from src.config import settings

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Manage encryption/decryption of sensitive data (Facebook tokens, cookies, etc.)"""

    def __init__(self):
        key = getattr(settings, "FERNET_KEY", None) or getattr(settings, "ENCRYPTION_KEY", None)
        if not key:
            # Dev fallback - generate one (do not use in production)
            import warnings
            from cryptography.fernet import Fernet
            key = Fernet.generate_key().decode()
            warnings.warn(
                f"FERNET_KEY not found in .env. Using generated dev key. "
                f"Add this to your .env: FERNET_KEY={key}",
                UserWarning
            )
        try:
            if isinstance(key, str):
                key = key.encode()
            self.cipher = Fernet(key)
        except Exception as e:
            logger.error(f"Failed to initialize Fernet cipher: {e}")
            raise

    def encrypt(self, data: str) -> str:
        """Encrypt a string. Returns base64 string."""
        if not data:
            return None
        try:
            return self.cipher.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, encrypted: str) -> str:
        """Decrypt a Fernet token back to string."""
        if not encrypted:
            return None
        try:
            return self.cipher.decrypt(encrypted.encode()).decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise

    def encrypt_dict(self, data: dict) -> dict:
        """Encrypt all string values in a dict (leaves non-strings untouched)."""
        if not data:
            return {}
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.encrypt(value)
            else:
                result[key] = value
        return result

    def decrypt_dict(self, data: dict) -> dict:
        """Decrypt values that look like Fernet tokens."""
        if not data:
            return {}
        result = {}
        for key, value in data.items():
            if isinstance(value, str) and value.startswith("gAAAAA"):
                try:
                    result[key] = self.decrypt(value)
                except Exception:
                    result[key] = value
            else:
                result[key] = value
        return result


# Singleton
encryption = EncryptionManager()
