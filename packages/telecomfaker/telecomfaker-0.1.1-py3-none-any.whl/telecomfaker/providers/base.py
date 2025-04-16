from abc import ABC, abstractmethod
from typing import Dict, Any

class DataProvider(ABC):
    """
    Abstract base class for telecom data providers.
    
    This class defines the interface that all data providers must implement.
    """
    
    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        """
        Get the telecom data from the provider.
        
        Returns:
            A dictionary containing telecom operator data
        
        Raises:
            Exception: If the data cannot be retrieved
        """
        pass