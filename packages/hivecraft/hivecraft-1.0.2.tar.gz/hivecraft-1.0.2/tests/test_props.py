"""Tests for property handlers."""
import os
import pytest
import xml.etree.ElementTree as ET
from hivecraft.props import MetaProps, DescProps
from hivecraft.props.meta.validators import is_iso_datetime_format, is_valid_uuid, is_semantic_version
from hivecraft.props.desc.validators import is_valid_difficulty, is_valid_language_code

def test_meta_props_init(temp_dir):
    """Test initializing MetaProps."""
    meta = MetaProps(temp_dir)
    assert meta.folder_name == temp_dir
    assert meta.file_name == os.path.join(temp_dir, "props", "meta.xml")

def test_desc_props_init(temp_dir):
    """Test initializing DescProps."""
    desc = DescProps(temp_dir)
    assert desc.folder_name == temp_dir
    assert desc.file_name == os.path.join(temp_dir, "props", "desc.xml")

def test_meta_props_check_file_integrity(temp_dir):
    """Test checking the integrity of meta.xml."""
    meta = MetaProps(temp_dir)
    meta.check_file_integrity()
    assert os.path.exists(os.path.join(temp_dir, "props", "meta.xml"))
    
    # Check that we can parse the file as XML
    tree = ET.parse(os.path.join(temp_dir, "props", "meta.xml"))
    root = tree.getroot()
    
    # Check that required fields exist
    for field in ["author", "created", "modified", "hivecraft_version", "title", "id"]:
        elem = root.find(".//{}".format(field), {"": "http://www.w3.org/2001/WMLSchema"})
        assert elem is not None, f"Field {field} not found in meta.xml"

def test_desc_props_check_file_integrity(temp_dir):
    """Test checking the integrity of desc.xml."""
    desc = DescProps(temp_dir)
    desc.check_file_integrity()
    assert os.path.exists(os.path.join(temp_dir, "props", "desc.xml"))
    
    # Check that we can parse the file as XML
    tree = ET.parse(os.path.join(temp_dir, "props", "desc.xml"))
    root = tree.getroot()
    
    # Check that required fields exist
    for field in ["difficulty", "language", "title", "index"]:
        elem = root.find(".//{}".format(field), {"": "http://www.w3.org/2001/WMLSchema"})
        assert elem is not None, f"Field {field} not found in desc.xml"

def test_meta_props_write_file(temp_dir):
    """Test writing meta.xml."""
    meta = MetaProps(temp_dir)
    meta.author = "Test Author"
    meta.title = "Test Title"
    meta.write_file()
    
    # Re-read the file and check values
    meta2 = MetaProps(temp_dir)
    meta2.check_file_integrity()
    assert meta2.author == "Test Author"
    assert meta2.title == "Test Title"

def test_desc_props_write_file(temp_dir):
    """Test writing desc.xml."""
    desc = DescProps(temp_dir)
    desc.difficulty = "HARD"
    desc.language = "fr"
    desc.title = "Test Title"
    desc.index = 42
    desc.write_file()
    
    # Re-read the file and check values
    desc2 = DescProps(temp_dir)
    desc2.check_file_integrity()
    assert desc2.difficulty == "HARD"
    assert desc2.language == "fr"
    assert desc2.title == "Test Title"
    assert desc2.index == 42

def test_validators():
    """Test the validator functions."""
    # Meta validators
    assert is_iso_datetime_format("2023-01-01T12:00:00Z") is True
    assert is_iso_datetime_format("invalid date") is False
    
    assert is_valid_uuid("123e4567-e89b-12d3-a456-426614174000") is True
    assert is_valid_uuid("invalid-uuid") is False
    
    assert is_semantic_version("1.0.0") is True
    assert is_semantic_version("v1.0") is False
    
    # Desc validators
    assert is_valid_difficulty("EASY") is True
    assert is_valid_difficulty("IMPOSSIBLE") is False
    
    assert is_valid_language_code("en") is True
    assert is_valid_language_code("english") is False
