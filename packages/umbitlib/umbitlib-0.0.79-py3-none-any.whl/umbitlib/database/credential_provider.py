import keyring
from typing import Optional, Dict
from urllib.parse import quote_plus

class CredentialProvider:  
    """Retrieves credentials from various sources."""

    def get_keyring_credentials(self, service_name: str, username: Optional[str] = None, encode_password: bool = True) -> Optional[Dict[str, str]]:
        """Retrieves credentials from the system's keyring."""
        try:
            credential_obj = keyring.get_credential(service_name, username)
            if credential_obj:
                password = quote_plus(credential_obj.password) if encode_password else credential_obj.password
                return {"username": credential_obj.username, "password": password}
            else:
                return None
        except Exception as e:
            print(f"Error retrieving credentials for service '{service_name}' and username '{username}': {e}")
            return None