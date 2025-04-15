from telecomfaker.providers.base import DataProvider
from telecomfaker.providers.local_json import LocalJsonProvider

# Keep StaticDataProvider for backward compatibility
StaticDataProvider = LocalJsonProvider

__all__ = ['DataProvider', 'LocalJsonProvider', 'StaticDataProvider']