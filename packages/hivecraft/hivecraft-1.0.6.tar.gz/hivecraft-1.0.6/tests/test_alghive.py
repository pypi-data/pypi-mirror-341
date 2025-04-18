"""Tests for the Alghive class."""
import os
import pytest
from hivecraft.alghive import Alghive

def test_init_valid_folder(valid_puzzle_dir):
    """Test initializing Alghive with a valid folder."""
    alghive = Alghive(valid_puzzle_dir)
    assert alghive.folder_name == valid_puzzle_dir

def test_init_invalid_folder():
    """Test initializing Alghive with a non-existent folder."""
    with pytest.raises(ValueError):
        Alghive("nonexistent_folder")

def test_check_integrity_valid(valid_puzzle_dir):
    """Test integrity check passes with valid puzzle."""
    alghive = Alghive(valid_puzzle_dir)
    # Should not raise an exception
    alghive.check_integrity()

def test_check_integrity_invalid(invalid_puzzle_dir):
    """Test integrity check fails with invalid puzzle."""
    alghive = Alghive(invalid_puzzle_dir)
    with pytest.raises(ValueError):
        alghive.check_integrity()

def test_zip_folder(valid_puzzle_dir):
    """Test zipping a puzzle folder."""
    alghive = Alghive(valid_puzzle_dir)
    alghive.zip_folder()
    zip_file_name = f"{os.path.basename(valid_puzzle_dir)}.alghive"
    assert os.path.exists(zip_file_name)
    # Cleanup
    os.remove(zip_file_name)

def test_run_tests(valid_puzzle_dir):
    """Test running tests on a valid puzzle."""
    alghive = Alghive(valid_puzzle_dir)
    # Should not raise an exception
    alghive.run_tests(2)

def test_generate_random_key():
    """Test generating a random key."""
    alghive = Alghive("dummy_dir", skip_folder_check=True)  # Skip directory check for this test
    key1 = alghive.generate_random_key()
    key2 = alghive.generate_random_key()
    assert isinstance(key1, str)
    assert len(key1) == 16
    # Keys should be different (probabilistically almost certain)
    assert key1 != key2
