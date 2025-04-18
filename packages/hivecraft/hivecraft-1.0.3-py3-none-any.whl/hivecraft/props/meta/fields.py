import datetime
import uuid
import getpass
from hivecraft.props.field_definition import FieldDefinition
from hivecraft.props.meta.validators import is_iso_datetime_format, is_valid_uuid, is_semantic_version, is_non_empty_string
from hivecraft.version import __version__ # Import package version

# Define default functions for dynamic values
def get_current_user() -> str:
    return getpass.getuser()

def get_current_iso_datetime() -> str:
    # Store in ISO 8601 format with UTC timezone indicator 'Z'
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_new_uuid() -> str:
    return str(uuid.uuid4())

# Define the fields for meta.xml
META_FIELDS = [
    FieldDefinition(name="author", data_type=str, required=True, validator=is_non_empty_string, default_value_factory=get_current_user),
    FieldDefinition(name="created", data_type=str, required=True, validator=is_iso_datetime_format, default_value_factory=get_current_iso_datetime),
    FieldDefinition(name="modified", data_type=str, required=True, validator=is_iso_datetime_format, default_value_factory=get_current_iso_datetime),
    FieldDefinition(name="hivecraft_version", data_type=str, required=True, validator=is_semantic_version, default_value=__version__),
    FieldDefinition(name="title", data_type=str, required=True, validator=is_non_empty_string, default_value="Meta"),
    FieldDefinition(name="id", data_type=str, required=True, validator=is_valid_uuid, default_value_factory=generate_new_uuid),
]

# Define the XML namespace (same as desc.xml)
XML_NAMESPACE = {"ns": "http://www.w3.org/2001/WMLSchema"}