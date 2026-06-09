"""
Encryption utilities for sensitive data (tokens, cookies, app secrets).
Uses Fernet (symmetric encryption from cryptography).
"""

import warnings
import logging
from typing import Optional

# Import Fernet với error handling
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    Fernet = None
    warnings.warn(
        "cryptography library not installed. Run: pip install cryptography",
        ImportWarning
    )

from src.config import settings

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Manage encryption/decryption of sensitive data (Facebook tokens, cookies, etc.)"""

    def __init__(self):
        """Initialize encryption manager with key from settings."""
        if not CRYPTO_AVAILABLE:
            raise ImportError(
                "cryptography is not installed. Please run: pip install cryptography"
            )
        
        # Get encryption key from settings
        key = getattr(settings, "FERNET_KEY", None) or getattr(settings, "ENCRYPTION_KEY", None)
        
        if not key:
            # Dev fallback - generate one (do not use in production)
            key = Fernet.generate_key().decode()
            warnings.warn(
                f"FERNET_KEY not found in .env. Using generated dev key. "
                f"Add this to your .env: FERNET_KEY={key}",
                UserWarning
            )
        
        # Ensure key is in bytes format
        if isinstance(key, str):
            key = key.encode()
        
        try:
            self.cipher = Fernet(key)
            logger.info("Encryption manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Fernet cipher: {e}")
            raise

    def encrypt(self, data: str) -> Optional[str]:
        """Encrypt a string. Returns base64 string."""
        if not data:
            return None
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, encrypted: str) -> Optional[str]:
        """Decrypt a Fernet token back to string."""
        if not encrypted:
            return None
        try:
            decrypted = self.cipher.decrypt(encrypted.encode())
            return decrypted.decode()
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
            # Fernet tokens typically start with "gAAAAA"
            if isinstance(value, str) and value.startswith("gAAAAA"):
                try:
                    result[key] = self.decrypt(value)
                except Exception:
                    # If decryption fails, keep original value
                    result[key] = value
            else:
                result[key] = value
        return result


# Singleton instance
try:
    encryption = EncryptionManager()
except Exception as e:
    logger.error(f"Failed to create encryption manager: {e}")
    encryption = None
    warnings.warn(
        "Encryption manager not available. Some features may not work.",
        RuntimeWarning
    )