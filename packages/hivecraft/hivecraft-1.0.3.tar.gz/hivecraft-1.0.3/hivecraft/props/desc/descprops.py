import os
import xml.etree.ElementTree as ET
from hivecraft.props.desc.fields import *

"""
desc.xml is a file that contains the basic properties related to the puzzle of the Alghive file
<Properties xmlns="http://www.w3.org/2001/WMLSchema">
    <difficulty>HARD</difficulty>
    <language>fr</language>
    <title>My Puzzle</title>
    <index>1</index>
</Properties>
"""
class DescProps:
    def __init__(self, folder_name: str):
        self.folder_name = folder_name
        self.props_dir = os.path.join(folder_name, "props")
        self.file_name = os.path.join(self.props_dir, "desc.xml")
        self._fields = {field.name: field for field in DESC_FIELDS}
        self._values = {field.name: field.default_value for field in DESC_FIELDS} # Initialize with default values
        
        for name, value in self._values.items():
            setattr(self, name, value)
            
    def _update_internal_values(self):
        """Updates internal dictionary from instance attributes."""
        for name in self._fields.keys():
            self._values[name] = getattr(self, name)

    def _update_attributes(self):
        """Updates instance attributes from internal dictionary."""
        for name, value in self._values.items():
            setattr(self, name, value)
        
    def check_file_integrity(self):
        """Checks if the file exists and is valid, creates/updates it otherwise."""
        os.makedirs(self.props_dir, exist_ok=True)
        
        if os.path.isfile(self.file_name):
            try:
                tree = ET.parse(self.file_name)
                root = tree.getroot()
                if not root.tag.endswith("Properties"):
                    raise ValueError(f"Invalid root tag in '{self.file_name}'. Expected 'Properties'.")
                
                parsed_values = {}
                for field_def in self._fields.values():
                    element = root.find(f"ns:{field_def.name}", XML_NAMESPACE)
                    parsed_values[field_def.name] = field_def.parse_and_validate(element)
                    
                self._values = parsed_values
                self._update_attributes()
            
            except ET.ParseError as e:
                raise ValueError(f"Error parsing XML file '{self.file_name}': {e}")
            except ValueError as e:
                raise ValueError(f"Invalid XML structure in '{self.file_name}': {e}")
            
        else:
            # File does not exist, create it with defaults
            print()
            print(f"> File '{self.file_name}' does not exist. Creating a default one.")
            print(f"  Defaults: difficulty='{self.difficulty}', language='{self.language}', title='{self.title}', index='{self.index}'")
            print()
            self.write_file() # Creates the file with default values
                
    def write_file(self):
        """Writes the current properties to the desc.xml file."""
        self._update_internal_values() # Ensure internal dict matches attributes before writing
        os.makedirs(self.props_dir, exist_ok=True) # Ensure props directory exists

        # Use the namespace in the root element
        root = ET.Element("Properties", xmlns=XML_NAMESPACE["ns"])

        for field_def in self._fields.values():
            # Create element without explicit namespace (will inherit from root)
            elem = ET.SubElement(root, field_def.name)
            value = self._values.get(field_def.name)
            # Convert value to string for XML text content
            elem.text = str(value) if value is not None else ""

        # Pretty print XML (optional)
        ET.indent(root, space="    ")
        tree = ET.ElementTree(root)
        # Add XML declaration and write
        tree.write(self.file_name, encoding='utf-8', xml_declaration=True)



