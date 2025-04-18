#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command-line interface for HiveCraft
"""

import argparse
import os
import sys
import zipfile
from hivecraft.alghive import Alghive
from hivecraft.version import __version__
from hivecraft.scripts import ForgeScript, DecryptScript, UnveilScript
from hivecraft.prompts import CipherPrompt, ObscurePrompt


def create_puzzle(args):
    """Creates a new puzzle folder with templates."""
    folder_name = args.name
    if os.path.exists(folder_name):
        if not args.force:
            print(f"Error: Folder '{folder_name}' already exists. Use --force to overwrite.")
            return 1
    
    os.makedirs(folder_name, exist_ok=True)
    os.makedirs(os.path.join(folder_name, "props"), exist_ok=True)
    
    # Create template files
    forge_script = ForgeScript(folder_name)
    decrypt_script = DecryptScript(folder_name)
    unveil_script = UnveilScript(folder_name)
    cipher_prompt = CipherPrompt(folder_name)
    obscure_prompt = ObscurePrompt(folder_name)
    
    # Write template content to files
    with open(os.path.join(folder_name, "forge.py"), 'w') as f:
        f.write(forge_script.generate_template())
    with open(os.path.join(folder_name, "decrypt.py"), 'w') as f:
        f.write(decrypt_script.generate_template())
    with open(os.path.join(folder_name, "unveil.py"), 'w') as f:
        f.write(unveil_script.generate_template())
    
    cipher_prompt.write_template()
    obscure_prompt.write_template()
    
    # Create a new Alghive instance to generate properties files
    alghive = Alghive(folder_name)
    alghive.meta_props.check_file_integrity()
    alghive.desc_props.check_file_integrity()
    
    print(f"Successfully created new puzzle in '{folder_name}'")
    return 0


def compile_puzzle(args):
    """Test Compiles a puzzle folder into an .alghive file."""
    folder_name = args.folder
    try:
        alghive = Alghive(folder_name)
        alghive.check_integrity()
        if not args.skip_test:
            alghive.run_tests(args.test_count)
        alghive.zip_folder()
        print(f"Successfully compiled '{folder_name}' into '{os.path.basename(folder_name)}.alghive'")
        return 0
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except RuntimeError as e:
        print(f"Error during execution: {e}")
        return 1


def extract_alghive(args):
    """Extracts an .alghive file to a folder."""
    file_path = args.file
    if not file_path.endswith('.alghive'):
        print(f"Error: File '{file_path}' is not an .alghive file.")
        return 1
    
    output_folder = args.output or os.path.splitext(os.path.basename(file_path))[0]
    if os.path.exists(output_folder) and not args.force:
        print(f"Error: Folder '{output_folder}' already exists. Use --force to overwrite.")
        return 1
    
    try:
        os.makedirs(output_folder, exist_ok=True)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        print(f"Successfully extracted '{file_path}' to '{output_folder}'")
        return 0
    except zipfile.BadZipFile:
        print(f"Error: '{file_path}' is not a valid zip file.")
        return 1
    except Exception as e:
        print(f"Error extracting file: {e}")
        return 1


def verify_puzzle(args):
    """Tests a puzzle folder."""
    folder_name = args.folder
    try:
        alghive = Alghive(folder_name)
        alghive.check_integrity()
        alghive.run_tests(args.count)
        print(f"All tests passed for '{folder_name}'")
        return 0
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except RuntimeError as e:
        print(f"Error during execution: {e}")
        return 1


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description=f"HiveCraft v{__version__} - AlgoHive puzzle management tool")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new puzzle folder')
    create_parser.add_argument('name', help='Name of the puzzle folder to create')
    create_parser.add_argument('--force', '-f', action='store_true', help='Force overwrite if folder exists')
    create_parser.set_defaults(func=create_puzzle)
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile a puzzle folder into an .alghive file')
    compile_parser.add_argument('folder', help='Path to the puzzle folder')
    compile_parser.add_argument('--test', '-t', action='store_true', help='Run tests before compiling')
    compile_parser.add_argument('--skip-test', '-s', action='store_true', help='Skip running tests before compiling')
    compile_parser.add_argument('--test-count', type=int, default=100, help='Number of tests to run (default: 5)')
    compile_parser.set_defaults(func=compile_puzzle)
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract an .alghive file to a folder')
    extract_parser.add_argument('file', help='Path to the .alghive file')
    extract_parser.add_argument('--output', '-o', help='Output folder (default: same as file name without extension)')
    extract_parser.add_argument('--force', '-f', action='store_true', help='Force overwrite if folder exists')
    extract_parser.set_defaults(func=extract_alghive)
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test a puzzle folder')
    test_parser.add_argument('folder', help='Path to the puzzle folder')
    test_parser.add_argument('--count', '-c', type=int, default=10, help='Number of tests to run (default: 10)')
    test_parser.set_defaults(func=verify_puzzle)

    # Version command is just a flag on the main parser
    parser.add_argument('--version', '-v', action='version', version=f'hivecraft {__version__}')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
