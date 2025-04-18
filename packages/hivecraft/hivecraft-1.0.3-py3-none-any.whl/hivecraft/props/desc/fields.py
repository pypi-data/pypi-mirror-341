from hivecraft.props.field_definition import FieldDefinition
from hivecraft.props.desc.validators import (
    is_valid_difficulty,
    is_valid_language_code,
    is_non_empty_string,
    is_positive_or_zero_int
)

"""
desc.xml is a file that contains the basic properties related to the puzzle of the Alghive file
<Properties xmlns="http://www.w3.org/2001/WMLSchema">
    <difficulty>HARD</difficulty>
    <language>fr</language>
    <title>My Puzzle</title>
    <index>1</index>
</Properties>
"""
DESC_FIELDS = [
    FieldDefinition(name="difficulty", data_type=str, required=True, default_value="EASY", validator=is_valid_difficulty),
    FieldDefinition(name="language", data_type=str, required=True, default_value="en", validator=is_valid_language_code),
    FieldDefinition(name="title", data_type=str, required=True, default_value="NO_TITLE", validator=is_non_empty_string),
    FieldDefinition(name="index", data_type=int, required=True, default_value=0, validator=is_positive_or_zero_int),
]

XML_NAMESPACE = { "ns": "http://www.w3.org/2001/WMLSchema" }