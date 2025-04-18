"""Tests for script handlers."""
import os
import pytest
from hivecraft.scripts import ForgeScript, DecryptScript, UnveilScript

def test_forge_script_init(valid_puzzle_dir):
    """Test initializing ForgeScript."""
    forge = ForgeScript(valid_puzzle_dir)
    assert forge.folder_name == valid_puzzle_dir
    assert forge.script_filename == "forge.py"
    assert forge.expected_class_name == "Forge"

def test_decrypt_script_init(valid_puzzle_dir):
    """Test initializing DecryptScript."""
    decrypt = DecryptScript(valid_puzzle_dir)
    assert decrypt.folder_name == valid_puzzle_dir
    assert decrypt.script_filename == "decrypt.py"
    assert decrypt.expected_class_name == "Decrypt"

def test_unveil_script_init(valid_puzzle_dir):
    """Test initializing UnveilScript."""
    unveil = UnveilScript(valid_puzzle_dir)
    assert unveil.folder_name == valid_puzzle_dir
    assert unveil.script_filename == "unveil.py"
    assert unveil.expected_class_name == "Unveil"

def test_forge_script_validate(valid_puzzle_dir):
    """Test validating a ForgeScript."""
    forge = ForgeScript(valid_puzzle_dir)
    assert forge.validate() is True

def test_decrypt_script_validate(valid_puzzle_dir):
    """Test validating a DecryptScript."""
    decrypt = DecryptScript(valid_puzzle_dir)
    assert decrypt.validate() is True

def test_unveil_script_validate(valid_puzzle_dir):
    """Test validating an UnveilScript."""
    unveil = UnveilScript(valid_puzzle_dir)
    assert unveil.validate() is True

def test_forge_script_run(valid_puzzle_dir):
    """Test running a ForgeScript."""
    forge = ForgeScript(valid_puzzle_dir)
    lines = forge.run(lines_count=5, unique_id="test_seed")
    assert isinstance(lines, list)
    assert len(lines) == 5
    assert all(isinstance(line, str) for line in lines)

def test_decrypt_script_run(valid_puzzle_dir):
    """Test running a DecryptScript."""
    decrypt = DecryptScript(valid_puzzle_dir)
    result = decrypt.run(lines=["test line"])
    assert result == "42"

def test_unveil_script_run(valid_puzzle_dir):
    """Test running an UnveilScript."""
    unveil = UnveilScript(valid_puzzle_dir)
    result = unveil.run(lines=["test line"])
    assert result == "24"

def test_script_validate_missing_file(temp_dir):
    """Test validating a script with a missing file."""
    forge = ForgeScript(temp_dir)
    assert forge.validate() is False

def test_generate_templates():
    """Test generating script templates."""
    forge = ForgeScript("dummy")
    decrypt = DecryptScript("dummy")
    unveil = UnveilScript("dummy")
    
    # Check that templates are non-empty strings
    assert isinstance(forge.generate_template(), str)
    assert isinstance(decrypt.generate_template(), str)
    assert isinstance(unveil.generate_template(), str)
    assert len(forge.generate_template()) > 0
    assert len(decrypt.generate_template()) > 0
    assert len(unveil.generate_template()) > 0
