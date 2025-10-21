"""
Amenity model for the HBnB application.
Represents an amenity that can be associated with places.
"""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity class representing a feature or service available at a place."""
    
    def __init__(self, name):
        """
        Initialize an Amenity instance.
        
        Args:
            name (str): The name of the amenity (max 50 characters)
        
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        self.name = self._validate_name(name)

    @staticmethod
    def _validate_name(name):
        """
        Validate amenity name.
        
        Args:
            name (str): The name to validate
        
        Returns:
            str: The validated name
        
        Raises:
            ValueError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(name) > 50:
            raise ValueError("Amenity name must be not exceed 50 characters")
        return name.strip()
    
    def __repr__(self):
        """String representation of the Amenity."""
        return f"<Amenity {self.id} - {self.name}>"