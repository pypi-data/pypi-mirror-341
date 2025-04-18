"""Tests for prompt file handlers."""
import os
import pytest
from hivecraft.prompts import CipherPrompt, ObscurePrompt

def test_cipher_prompt_init(valid_puzzle_dir):
    """Test initializing CipherPrompt."""
    cipher = CipherPrompt(valid_puzzle_dir)
    assert cipher.folder_name == valid_puzzle_dir
    assert cipher.filename == "cipher.html"

def test_obscure_prompt_init(valid_puzzle_dir):
    """Test initializing ObscurePrompt."""
    obscure = ObscurePrompt(valid_puzzle_dir)
    assert obscure.folder_name == valid_puzzle_dir
    assert obscure.filename == "obscure.html"

def test_cipher_prompt_validate(valid_puzzle_dir):
    """Test validating a CipherPrompt."""
    cipher = CipherPrompt(valid_puzzle_dir)
    assert cipher.validate() is True

def test_obscure_prompt_validate(valid_puzzle_dir):
    """Test validating an ObscurePrompt."""
    obscure = ObscurePrompt(valid_puzzle_dir)
    assert obscure.validate() is True

def test_prompt_validate_missing_file(temp_dir):
    """Test validating a prompt with a missing file."""
    cipher = CipherPrompt(temp_dir)
    assert cipher.validate() is False

def test_prompt_validate_invalid_content(temp_dir):
    """Test validating a prompt with invalid content."""
    # Create a file without article tags
    with open(os.path.join(temp_dir, "cipher.html"), 'w') as f:
        f.write("<p>Invalid content without article tags</p>")
    
    cipher = CipherPrompt(temp_dir)
    assert cipher.validate() is False

def test_generate_templates():
    """Test generating prompt templates."""
    cipher = CipherPrompt("dummy")
    obscure = ObscurePrompt("dummy")
    
    # Check that templates are non-empty strings
    assert isinstance(cipher.generate_template(), str)
    assert isinstance(obscure.generate_template(), str)
    assert len(cipher.generate_template()) > 0
    assert len(obscure.generate_template()) > 0

def test_write_template(temp_dir):
    """Test writing a template to a file."""
    cipher = CipherPrompt(temp_dir)
    cipher.write_template()
    assert os.path.exists(os.path.join(temp_dir, "cipher.html"))
    
    # Check content contains article tags
    with open(os.path.join(temp_dir, "cipher.html"), 'r') as f:
        content = f.read()
        assert content.startswith("<article>")
        assert content.endswith("</article>\n")
