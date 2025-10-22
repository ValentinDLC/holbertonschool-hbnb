"""
Base model class for all entities in the HBnb application.
Provides common attributes and methods for all models.
"""
import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models with common attributes."""
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary.
        
        Args:
            data (dict): Dictionnary containing the attributes to update
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"