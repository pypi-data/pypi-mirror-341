"""
Data models for the QuantPlay API client.
Defines the structure of API responses and requests.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, ClassVar, Type, TypeVar, cast



T = TypeVar('T', bound='BaseModel')


@dataclass
class BaseModel:
    """Base model with common functionality for all models."""
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create an instance from a dictionary."""
        # Filter out keys that are not fields in the dataclass
        field_names = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert instance to a dictionary."""
        return asdict(self)
    
    @classmethod
    def from_json_list(cls: Type[T], json_data: List[Dict[str, Any]]) -> List[T]:
        """Create a list of instances from a JSON array."""
        return [cls.from_dict(item) for item in json_data]




@dataclass
class Account(BaseModel):
    """Trading account information."""
    broker: str
    username: str
    nickname: str
    expiry: str

    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """Create an Account instance from a dictionary with nested objects."""
        account_data = data.copy()

        
        # Filter out keys that are not fields in the dataclass
        field_names = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore
        filtered_data = {k: v for k, v in account_data.items() if k in field_names}
        
        return cls(**filtered_data)


@dataclass
class APIResponse(BaseModel):
    """Generic API response model."""
    status: str
    data: Any
    message: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'APIResponse':
        """Create an APIResponse instance from a dictionary."""
        return cls(**data)




