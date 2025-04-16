import json
import os
import pkg_resources

class LocalJsonProvider:
    """Provider that loads telecom operator data from a local JSON file."""
    
    def __init__(self, file_path=None):
        """
        Initialize the provider with a file path.
        
        Args:
            file_path: Path to the JSON file. If None, uses the default data file.
        """
        self.file_path = file_path or self._get_default_data_path()
        self.data = None
    
    def _get_default_data_path(self):
        """Get the path to the default data file included with the package."""
        # Use pkg_resources to find the file within the package
        return pkg_resources.resource_filename('telecomfaker', 'data/telecom_data.json')
    
    def get_data(self):
        """
        Load and return the data from the JSON file.
        
        Returns:
            A dictionary containing the loaded data
            
        Raises:
            FileNotFoundError: If the JSON file doesn't exist
            json.JSONDecodeError: If the JSON file is invalid
        """
        if self.data is None:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Data file not found: {self.file_path}")
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in data file: {self.file_path}")
        
        return self.data 