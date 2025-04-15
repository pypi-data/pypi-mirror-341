from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class OperatorSize(str, Enum):
    """Enum representing the size of a telecom operator."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class TelecomOperator(BaseModel):
    """
    Pydantic model representing a telecom operator.
    
    This model provides validation and serialization for telecom operator data.
    """
    name: str = Field(..., description="The name of the telecom operator")
    country: str = Field(..., description="The country where the operator is based")
    mcc: str = Field(..., description="Mobile Country Code (MCC)")
    mnc: str = Field(..., description="Mobile Network Code (MNC)")
    size: OperatorSize = Field(default=OperatorSize.MEDIUM, description="Size of the operator")
    is_mvno: bool = Field(default=False, description="Whether the operator is a Mobile Virtual Network Operator")
    
    class Config:
        """Configuration for the TelecomOperator model."""
        schema_extra = {
            "example": {
                "name": "Vodafone",
                "country": "Germany",
                "mcc": "262",
                "mnc": "02",
                "size": "large",
                "is_mvno": False
            }
        } 