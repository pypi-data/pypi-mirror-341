"""Tests for the field definition classes."""
import pytest
import xml.etree.ElementTree as ET
from hivecraft.props.field_definition import FieldDefinition

def test_field_definition_init():
    """Test initializing a FieldDefinition."""
    field = FieldDefinition(name="test", data_type=str, required=True)
    assert field.name == "test"
    assert field.data_type == str
    assert field.required is True

def test_field_definition_default_value():
    """Test default value handling."""
    # Static default
    field1 = FieldDefinition(name="test1", data_type=str, default_value="default")
    assert field1.default_value == "default"
    
    # Factory default
    field2 = FieldDefinition(name="test2", data_type=int, default_value_factory=lambda: 42)
    assert field2.default_value == 42
    
    # No defaults
    field3 = FieldDefinition(name="test3", data_type=str)
    assert field3.default_value is None

def test_field_definition_both_defaults():
    """Test that providing both default types raises an error."""
    with pytest.raises(ValueError):
        FieldDefinition(name="test", data_type=str, default_value="default", default_value_factory=lambda: "factory")

def test_parse_and_validate_missing_required():
    """Test parsing a missing required element."""
    field = FieldDefinition(name="test", data_type=str, required=True)
    with pytest.raises(ValueError):
        field.parse_and_validate(None)

def test_parse_and_validate_missing_optional():
    """Test parsing a missing optional element."""
    field = FieldDefinition(name="test", data_type=str, required=False, default_value="default")
    assert field.parse_and_validate(None) == "default"

def test_parse_and_validate_with_element():
    """Test parsing an element with text."""
    field = FieldDefinition(name="test", data_type=int, required=True)
    element = ET.Element("test")
    element.text = "42"
    assert field.parse_and_validate(element) == 42

def test_parse_and_validate_with_validator():
    """Test parsing with a validator function."""
    def validate_positive(value):
        return value > 0
    
    field = FieldDefinition(name="test", data_type=int, required=True, validator=validate_positive)
    
    # Valid value
    element1 = ET.Element("test")
    element1.text = "42"
    assert field.parse_and_validate(element1) == 42
    
    # Invalid value
    element2 = ET.Element("test")
    element2.text = "-42"
    with pytest.raises(ValueError):
        field.parse_and_validate(element2)
