from base_model import BaseModel
from user import User

class Place(BaseModel):
    """
    User class that inherits from BaseModel.
    """
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a Place instance with title, description, price, latitude,
        longitude, and owner.
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude


