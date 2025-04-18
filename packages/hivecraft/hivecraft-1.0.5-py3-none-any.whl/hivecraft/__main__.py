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


# ANSI escape codes for colors
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"


def create_puzzle(args):
    """Creates a new puzzle folder with templates."""
    folder_name = args.name
    if os.path.exists(folder_name):
        if not args.force:
            print(COLOR_RED + f"Error: Folder '{folder_name}' already exists. Use --force to overwrite." + COLOR_RESET)
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
    
    print(COLOR_GREEN + f"Successfully created new puzzle in '{folder_name}'" + COLOR_RESET)
    return 0


def _compile_single_puzzle(folder_name, skip_test=False, test_count=100):
    """Compiles a single puzzle folder. Returns True on success, False on failure."""
    try:
        alghive = Alghive(folder_name)
        alghive.check_integrity()
        if not skip_test:
            alghive.run_tests(test_count)
        alghive.zip_folder()
        print(COLOR_GREEN + f"Successfully compiled '{folder_name}' into '{os.path.basename(folder_name)}.alghive'" + COLOR_RESET)
        return True
    except ValueError as e:
        print(COLOR_RED + f"Error compiling '{folder_name}': {e}" + COLOR_RESET)
        return False
    except RuntimeError as e:
        print(COLOR_RED + f"Error during execution for '{folder_name}': {e}" + COLOR_RESET)
        return False
    except FileNotFoundError:
        print(COLOR_RED + f"Error: Folder '{folder_name}' or required files not found." + COLOR_RESET)
        return False
    except Exception as e:
        print(COLOR_RED + f"An unexpected error occurred for '{folder_name}': {e}" + COLOR_RESET)
        return False


def compile_puzzle(args):
    """Compiles a puzzle folder into an .alghive file."""
    folder_name = args.folder
    if not os.path.isdir(folder_name):
        print(COLOR_RED + f"Error: '{folder_name}' is not a valid directory." + COLOR_RESET)
        return 1

    if _compile_single_puzzle(folder_name, args.skip_test, args.test_count):
        return 0
    else:
        return 1


def compile_all_puzzles(args):
    """Compiles all puzzle folders within a given directory."""
    base_directory = args.directory
    if not os.path.isdir(base_directory):
        print(COLOR_RED + f"Error: '{base_directory}' is not a valid directory." + COLOR_RESET)
        return 1

    success_count = 0
    fail_count = 0
    total_count = 0

    print(f"Scanning directory '{base_directory}' for puzzle folders...")

    for item in os.listdir(base_directory):
        item_path = os.path.join(base_directory, item)
        if os.path.isdir(item_path):
            # Basic check: does it look like a puzzle folder? (e.g., contains forge.py)
            # You might want a more robust check here.
            if os.path.exists(os.path.join(item_path, 'forge.py')):
                print(f"\nAttempting to compile '{item_path}'...")
                total_count += 1
                if _compile_single_puzzle(item_path, args.skip_test, args.test_count):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                print(COLOR_YELLOW + f"Skipping '{item_path}': Does not appear to be a puzzle folder (missing forge.py)." + COLOR_RESET)

    print("\n--- Compilation Summary ---")
    print(f"Total folders processed: {total_count}")
    print(COLOR_GREEN + f"Successful compilations: {success_count}" + COLOR_RESET)
    print(COLOR_RED + f"Failed compilations: {fail_count}" + COLOR_RESET)

    return 1 if fail_count > 0 else 0


def extract_alghive(args):
    """Extracts an .alghive file to a folder."""
    file_path = args.file
    if not file_path.endswith('.alghive'):
        print(COLOR_RED + f"Error: File '{file_path}' is not an .alghive file." + COLOR_RESET)
        return 1
    
    output_folder = args.output or os.path.splitext(os.path.basename(file_path))[0]
    if os.path.exists(output_folder) and not args.force:
        print(COLOR_RED + f"Error: Folder '{output_folder}' already exists. Use --force to overwrite." + COLOR_RESET)
        return 1
    
    try:
        os.makedirs(output_folder, exist_ok=True)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        print(COLOR_GREEN + f"Successfully extracted '{file_path}' to '{output_folder}'" + COLOR_RESET)
        return 0
    except zipfile.BadZipFile:
        print(COLOR_RED + f"Error: '{file_path}' is not a valid zip file." + COLOR_RESET)
        return 1
    except Exception as e:
        print(COLOR_RED + f"Error extracting file: {e}" + COLOR_RESET)
        return 1


def verify_puzzle(args):
    """Tests a puzzle folder."""
    folder_name = args.folder
    try:
        alghive = Alghive(folder_name)
        alghive.check_integrity()
        alghive.run_tests(args.count)
        print(COLOR_GREEN + f"All tests passed for '{folder_name}'" + COLOR_RESET)
        return 0
    except ValueError as e:
        print(COLOR_RED + f"Error: {e}" + COLOR_RESET)
        return 1
    except RuntimeError as e:
        print(COLOR_RED + f"Error during execution: {e}" + COLOR_RESET)
        return 1


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description=f"HiveCraft v{__version__} - AlgoHive puzzle management tool")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute', required=True)

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new puzzle folder')
    create_parser.add_argument('name', help='Name of the puzzle folder to create')
    create_parser.add_argument('--force', '-f', action='store_true', help='Force overwrite if folder exists')
    create_parser.set_defaults(func=create_puzzle)
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile a single puzzle folder into an .alghive file')
    compile_parser.add_argument('folder', help='Path to the puzzle folder')
    compile_parser.add_argument('--skip-test', '-s', action='store_true', help='Skip running tests before compiling')
    compile_parser.add_argument('--test-count', type=int, default=100, help='Number of tests to run (default: 100)')
    compile_parser.set_defaults(func=compile_puzzle)

    # Compile All command
    compile_all_parser = subparsers.add_parser('compile-all', help='Compile all puzzle folders within a directory')
    compile_all_parser.add_argument('directory', help='Path to the directory containing puzzle folders')
    compile_all_parser.add_argument('--skip-test', '-s', action='store_true', help='Skip running tests before compiling')
    compile_all_parser.add_argument('--test-count', type=int, default=100, help='Number of tests to run (default: 100)')
    compile_all_parser.set_defaults(func=compile_all_puzzles)

    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract an .alghive file to a folder')
    extract_parser.add_argument('file', help='Path to the .alghive file')
    extract_parser.add_argument('--output', '-o', help='Output folder (default: same as file name without extension)')
    extract_parser.add_argument('--force', '-f', action='store_true', help='Force overwrite if folder exists')
    extract_parser.set_defaults(func=extract_alghive)
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test a puzzle folder')
    test_parser.add_argument('folder', help='Path to the puzzle folder')
    test_parser.add_argument('--count', '-c', type=int, default=100, help='Number of tests to run (default: 100)')
    test_parser.set_defaults(func=verify_puzzle)

    # Version command is just a flag on the main parser
    parser.add_argument('--version', '-v', action='version', version=f'hivecraft {__version__}')
    
    args = parser.parse_args()
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
