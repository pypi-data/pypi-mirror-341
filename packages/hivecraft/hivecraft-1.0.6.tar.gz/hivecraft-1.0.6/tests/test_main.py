"""Tests for the command-line interface."""
import os
import sys
import subprocess
import pytest
from unittest import mock
from hivecraft.__main__ import create_puzzle, compile_puzzle, extract_alghive, verify_puzzle, main

def test_create_puzzle(temp_dir):
    """Test creating a puzzle."""
    # Create a valid name in the temp directory
    name = os.path.join(temp_dir, "test_puzzle")
    
    # Mock args
    args = mock.Mock()
    args.name = name
    args.force = False
    
    # Call create_puzzle
    result = create_puzzle(args)
    assert result == 0
    
    # Check that expected files were created
    assert os.path.exists(name)
    assert os.path.exists(os.path.join(name, "forge.py"))
    assert os.path.exists(os.path.join(name, "decrypt.py"))
    assert os.path.exists(os.path.join(name, "unveil.py"))
    assert os.path.exists(os.path.join(name, "cipher.html"))
    assert os.path.exists(os.path.join(name, "obscure.html"))
    assert os.path.exists(os.path.join(name, "props", "meta.xml"))
    assert os.path.exists(os.path.join(name, "props", "desc.xml"))

def test_create_puzzle_existing_no_force(temp_dir):
    """Test creating a puzzle with existing folder without force."""
    # Create the directory first
    name = os.path.join(temp_dir, "test_existing")
    os.makedirs(name, exist_ok=True)
    
    # Mock args
    args = mock.Mock()
    args.name = name
    args.force = False
    
    # Call create_puzzle
    result = create_puzzle(args)
    assert result == 1  # Expect failure

def test_create_puzzle_existing_with_force(temp_dir):
    """Test creating a puzzle with existing folder with force."""
    # Create the directory first
    name = os.path.join(temp_dir, "test_force")
    os.makedirs(name, exist_ok=True)
    
    # Mock args
    args = mock.Mock()
    args.name = name
    args.force = True
    
    # Call create_puzzle
    result = create_puzzle(args)
    assert result == 0  # Expect success

def test_compile_puzzle(valid_puzzle_dir):
    """Test compiling a puzzle."""
    # Mock args
    args = mock.Mock()
    args.folder = valid_puzzle_dir
    args.test = False
    
    # Call compile_puzzle
    result = compile_puzzle(args)
    assert result == 0
    
    # Check that the .alghive file was created
    expected_file = f"{os.path.basename(valid_puzzle_dir)}.alghive"
    assert os.path.exists(expected_file)
    
    # Cleanup
    if os.path.exists(expected_file):
        os.remove(expected_file)

def test_compile_puzzle_with_test(valid_puzzle_dir):
    """Test compiling a puzzle with testing."""
    # Mock args
    args = mock.Mock()
    args.folder = valid_puzzle_dir
    args.test = True
    args.test_count = 1
    
    # Call compile_puzzle
    result = compile_puzzle(args)
    assert result == 0
    
    # Cleanup
    expected_file = f"{os.path.basename(valid_puzzle_dir)}.alghive"
    if os.path.exists(expected_file):
        os.remove(expected_file)

def test_extract_alghive(alghive_file, temp_dir):
    """Test extracting an .alghive file."""
    output_folder = os.path.join(temp_dir, "extracted")
    
    # Mock args
    args = mock.Mock()
    args.file = alghive_file
    args.output = output_folder
    args.force = False
    
    # Call extract_alghive
    result = extract_alghive(args)
    assert result == 0
    
    # Check that the folder was created with expected files
    assert os.path.exists(output_folder)
    assert os.path.exists(os.path.join(output_folder, "forge.py"))
    assert os.path.exists(os.path.join(output_folder, "decrypt.py"))
    assert os.path.exists(os.path.join(output_folder, "unveil.py"))

def test_extract_alghive_existing_folder(alghive_file, temp_dir):
    """Test extracting to an existing folder without force."""
    output_folder = os.path.join(temp_dir, "existing_extract")
    os.makedirs(output_folder, exist_ok=True)
    
    # Mock args
    args = mock.Mock()
    args.file = alghive_file
    args.output = output_folder
    args.force = False
    
    # Call extract_alghive
    result = extract_alghive(args)
    assert result == 1  # Expect failure

def test_verify_puzzle(valid_puzzle_dir):
    """Test testing a puzzle."""
    # Mock args
    args = mock.Mock()
    args.folder = valid_puzzle_dir
    args.count = 1
    
    # Call verify_puzzle
    result = verify_puzzle(args)
    assert result == 0

def test_main_version():
    """Test the main function with --version flag."""
    # This is a subprocess test since we're checking sys.exit behavior
    result = subprocess.run([sys.executable, "-m", "hivecraft", "--version"], 
                            capture_output=True, text=True)
    assert "hivecraft" in result.stdout.lower()

def test_main_help():
    """Test the main function with --help flag."""
    # This is a subprocess test since we're checking sys.exit behavior
    result = subprocess.run([sys.executable, "-m", "hivecraft", "--help"], 
                            capture_output=True, text=True)
    assert "usage" in result.stdout.lower()
    assert "HiveCraft" in result.stdout
