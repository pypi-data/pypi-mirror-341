import datetime
import uuid
import re

def is_iso_datetime_format(value: str) -> bool:
    """Checks if the string is in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ or similar)."""
    try:
        # Attempt to parse, allowing for timezone offsets
        datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def is_valid_uuid(value: str) -> bool:
    """Checks if the string is a valid UUID."""
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False

def is_semantic_version(value: str) -> bool:
    """Checks if the string follows basic semantic versioning (e.g., X.Y.Z)."""
    pattern = r"^\d+\.\d+\.\d+([\-\+].+)?$" # Allows for pre-release/build metadata
    return bool(re.match(pattern, value))

def is_non_empty_string(value: str) -> bool:
    """Checks if the value is a non-empty string."""
    return isinstance(value, str) and bool(value.strip())