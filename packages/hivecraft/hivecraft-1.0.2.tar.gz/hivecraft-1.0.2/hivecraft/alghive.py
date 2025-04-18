import os
import random
import string
import zipfile
import sys
import time
from hivecraft.props import *
from hivecraft.scripts import *
from hivecraft.prompts import *

class Alghive:
    EXTENSION = '.alghive'
    EXECUTABLES_REQUIRED = ["forge.py", "decrypt.py", "unveil.py"]
    PROMPTS_REQUIRED = ["cipher.html", "obscure.html"]
    PROPS_FOLDER = "props"

    def __init__(self, folder_name, skip_folder_check=False):
        if not skip_folder_check and not os.path.isdir(folder_name):
            raise ValueError(f"The folder '{folder_name}' does not exist.")

        self.folder_name = folder_name.rstrip("/")
        self.zip_file_name = f"{folder_name}{self.EXTENSION}"

        # Instantiate script handlers
        self.forge = ForgeScript(self.folder_name)
        self.decrypt = DecryptScript(self.folder_name)
        self.unveil = UnveilScript(self.folder_name)
        
        # Instantiate prompt handlers
        self.cipher_prompt = CipherPrompt(self.folder_name)
        self.obscure_prompt = ObscurePrompt(self.folder_name)

        # Instantiate property handlers
        self.meta_props = MetaProps(self.folder_name)
        self.desc_props = DescProps(self.folder_name)

    def check_integrity(self):
        # If one of the checks fails, raise an exception
        if not self.check_files():
            raise ValueError(f"Folder '{self.folder_name}' does not respect the file constraints.")

        if not self.forge.validate():
            raise ValueError(f"Folder '{self.folder_name}' does not respect the forge constraints.")

        if not self.decrypt.validate():
            raise ValueError(f"Folder '{self.folder_name}' does not respect the decrypt constraints.")

        if not self.unveil.validate():
            raise ValueError(f"Folder '{self.folder_name}' does not respect the unveil constraints.")

        if not self.cipher_prompt.validate():
            raise ValueError(f"Folder '{self.folder_name}' does not respect the cipher prompt constraints.")
        
        if not self.obscure_prompt.validate():
            raise ValueError(f"Folder '{self.folder_name}' does not respect the obscure prompt constraints.")

        try:
            self.desc_props.check_file_integrity()
            self.meta_props.check_file_integrity()
        except ValueError as e:
            raise ValueError(f"Folder '{self.folder_name}' does not respect the props constraints: {e}")


    def check_files(self):
        # Check if all required files are present
        FILES_REQUIRED = self.EXECUTABLES_REQUIRED + self.PROMPTS_REQUIRED
        for file in FILES_REQUIRED:
            if not os.path.isfile(os.path.join(self.folder_name, file)):
                print(f"> Error: File '{file}' is missing in the folder '{self.folder_name}'.")
                return False

        return True

    def zip_folder(self):
        # Create the zip file name with .alghive extension
        file_name = os.path.basename(self.folder_name) # Use basename for the zip filename
        zip_file_name = f"{file_name}{self.EXTENSION}"

        # Ensure properties are written before zipping
        self.meta_props.write_file()
        self.desc_props.write_file()

        # Create a zip file with .alghive extension
        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.folder_name):
                # Exclude __pycache__ directories
                dirs[:] = [d for d in dirs if d != '__pycache__']
                for file in files:
                    # Exclude .pyc files
                    if file.endswith('.pyc'):
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=self.folder_name)
                    zipf.write(file_path, arcname)

    def run_tests(self, count):
        print(f"Running {count} tests...")
        
        # Setup progress bar
        bar_length = 40
        failed = 0
        
        # Run tests with progress bar
        for i in range(count):
            # Update progress bar
            progress = (i + 1) / count
            block = int(round(bar_length * progress))
            progress_bar = "[" + "=" * block + " " * (bar_length - block) + "]"
            percent = int(round(progress * 100))
            
            # Print the progress bar and overwrite the same line
            sys.stdout.write(f"\r  Progress: {progress_bar} {percent}% ({i+1}/{count})")
            sys.stdout.flush()
            
            try:
                random_key = self.generate_random_key()
                lines = self.forge.run(lines_count=100, unique_id=random_key)
                self.decrypt.run(lines=lines)
                self.unveil.run(lines=lines)
            except (RuntimeError, FileNotFoundError, ImportError, AttributeError, TypeError, Exception) as e:
                failed += 1
                print(f"\n> Test {i+1} failed: {e}")
                raise RuntimeError(f"Test failed during execution.") from e
        
        # Move to next line after progress bar completion
        print()
        print(f"All {count} tests passed successfully.")

    def generate_random_key(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))





