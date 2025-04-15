import json
import os
from typing import Dict, Any

from telecomfaker.providers.base import DataProvider

class LocalJsonProvider(DataProvider):
    """
    A data provider that loads telecom data from a local JSON file.
    """
    
    def __init__(self, data_path: str = None):
        """
        Initialize the local JSON data provider.
        
        Args:
            data_path: Path to the JSON data file. If None, uses the default path.
        """
        self.data_path = data_path or self._get_default_data_path()
        self.data = self.load_data()
    
    def _get_default_data_path(self) -> str:
        """
        Get the default path to the telecom data JSON file.
        
        Returns:
            The path to the default data file
        """
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'data',
            'telecom_data.json'
        )
    
    def load_data(self) -> Dict[str, Any]:
        """
        Load the telecom data from the JSON file.
        
        Returns:
            A dictionary containing the telecom data
            
        Raises:
            FileNotFoundError: If the data file cannot be found
            json.JSONDecodeError: If the data file contains invalid JSON
        """
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Telecom data source not found at {self.data_path}. "
                f"Please check the data source path and ensure it exists."
            )
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid JSON in telecom data source at {self.data_path}. "
                f"Please check the data source format."
            )
    
    def get_data(self) -> Dict[str, Any]:
        """
        Get the telecom data.
        
        Returns:
            A dictionary containing telecom operator data
            
        Raises:
            Exception: If the data cannot be retrieved
        """
        if not self.data:
            # Reload the data if it's not available
            self.data = self.load_data()
        
        return self.data 