import re
import uuid
from copy import deepcopy

from cryptography.fernet import Fernet
from fastapi import Request

from common.config import common_settings
from common.services import ServiceType


def validate_identifier(identifier: str) -> str:
    """Validates and normalizes account identifiers to match GitHub repository naming conventions.

    Args:
        identifier: The account identifier to validate

    Returns:
        Normalized (lowercase) identifier if valid

    Raises:
        ValueError: If the identifier is invalid
    """
    if not identifier:
        raise ValueError("identifier cannot be empty")

    # Check for valid characters and pattern
    if not re.match(
        r"^[a-zA-Z0-9][a-zA-Z0-9-_]*[a-zA-Z0-9]$|^[a-zA-Z0-9]$", identifier
    ):
        raise ValueError(
            "identifier must contain only alphanumeric characters, hyphens, or "
            "underscores, and cannot start or end with a hyphen"
        )

    # Check for consecutive hyphens
    if "--" in identifier:
        raise ValueError("identifier cannot contain consecutive hyphens")

    return identifier.lower()  # normalize to lowercase for consistency


def email_to_username(email: str) -> str:
    """Converts an email address to a valid username.

    Args:
        email: Email address to convert

    Returns:
        A valid username derived from the email address

    Raises:
        ValueError: If a valid username cannot be generated from the email
    """
    if not email or "@" not in email:
        raise ValueError("Invalid email address")

    # Get the part before @ and replace invalid chars with underscore
    username = email.split("@")[0]
    username = re.sub(r"[^a-zA-Z0-9-]", "_", username)

    # Remove consecutive underscores
    username = re.sub(r"_+", "_", username)

    # Ensure it starts and ends with alphanumeric
    username = username.strip("_-")

    # If empty after cleaning, raise error
    if not username:
        raise ValueError("Could not generate valid username from email")

    # Validate and normalize using existing function
    return validate_identifier(username)


def extract_access_token(request: Request) -> str | None:
    token_string = request.headers.get(common_settings.ACCESS_TOKEN_HEADER)
    if token_string is None:
        return None
    return token_string.split(" ")[-1]


def extract_service_key(request: Request) -> str | None:
    key_string = request.headers.get(common_settings.SERVICE_KEY_HEADER)
    if key_string is None:
        return None
    return key_string


def extract_service_type(request: Request) -> str | None:
    from common.services import ServiceType

    type_string = request.headers.get(common_settings.SERVICE_TYPE_HEADER)
    if type_string is None:
        return None
    return ServiceType(type_string).value


def imbue_header_with_access_token(
    token: str, headers: dict, in_place: bool = True
) -> dict:
    if not in_place:
        headers = deepcopy(headers)
    headers[common_settings.ACCESS_TOKEN_HEADER] = f"Bearer {token}"
    return headers


def imbue_header_with_service_key(
    key: str, headers: dict, in_place: bool = True
) -> dict:
    if not in_place:
        headers = deepcopy(headers)
    headers[common_settings.SERVICE_KEY_HEADER] = key
    return headers


def imbue_header_with_service_type(
    service_type: str | ServiceType, headers: dict, in_place: bool = True
) -> dict:
    if not in_place:
        headers = deepcopy(headers)
    headers[common_settings.SERVICE_TYPE_HEADER] = ServiceType(service_type).value
    return headers


def generate_encryption_key() -> str:
    """Generate a new encryption key as a string.

    Returns:
        str: A new encryption key ready for storage
    """
    return Fernet.generate_key().decode()


def encrypt_text(text: str, key: str) -> str:
    """Encrypt a string using a key.

    Args:
        text: The text to encrypt
        key: The encryption key as a string

    Returns:
        str: The encrypted text

    Raises:
        ValueError: If the key is invalid
    """
    f = Fernet(key.encode())
    encrypted_data = f.encrypt(text.encode())
    return encrypted_data.decode()


def decrypt_text(encrypted_text: str, key: str) -> str:
    """Decrypt an encrypted string using a key.

    Args:
        encrypted_text: The text to decrypt
        key: The encryption key as a string

    Returns:
        str: The decrypted text

    Raises:
        ValueError: If the key is invalid or the text can't be decrypted
    """
    try:
        f = Fernet(key.encode())
        decrypted_data = f.decrypt(encrypted_text.encode())
        return decrypted_data.decode()
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}") from e
