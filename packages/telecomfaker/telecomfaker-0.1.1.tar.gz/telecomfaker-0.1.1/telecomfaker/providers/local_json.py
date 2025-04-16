import json
import pkg_resources
from typing import Dict, Any

from telecomfaker.providers.base import DataProvider

class LocalJsonProvider(DataProvider):
    """
    A data provider that loads telecom data from a local JSON file.
    """
    
    def __init__(self, file_path=None):
        """
        Initialize the local JSON data provider.
        
        Args:
            file_path: Path to the JSON data file. If None, uses the default path.
        """
        self.file_path = file_path or self._get_default_data_path()
        self.data = None
    
    def _get_default_data_path(self):
        """
        Get the default path to the telecom data JSON file.
        
        Returns:
            The path to the default data file
        """
        return pkg_resources.resource_filename('telecomfaker', 'data/telecom_data.json')
    
    def get_data(self) -> Dict[str, Any]:
        """
        Get the telecom data.
        
        Returns:
            A dictionary containing telecom operator data
            
        Raises:
            Exception: If the data cannot be retrieved
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