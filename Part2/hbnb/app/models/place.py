"""
Place model for the HBnB application.
Represents a place that can be rented.
"""
from app.models.base_model import BaseModel


class Place(BaseModel):
    """Place class representing a rentable property."""
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a Place instance.
        
        Args:
            title (str): Title of the place (max 100 characters)
            description (str): Detailed description (optional)
            price (float): Price per night (must be positive)
            latitude (float): Latitude coordinate (-90.0 to 90.0)
            longitude (float): Longitude coordinate (-180.0 to 180.0)
            owner (User): User instance who owns the place
        
        Raises:
            ValueError: If validation fails for any attribute
        """
        super().__init__()
        self.title = self._validate_title(title)
        self.description = description or ""
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = self._validate_owner(owner)
        self.reviews = []  # List to store reviews for this place
        self.amenities = []  # List to store amenities for this place
        
        # Add this place to the owner's list of places
        if hasattr(owner, 'add_place'):
            owner.add_place(self)

    @staticmethod
    def _validate_title(title):
        """
        Validate place title.
        
        Args:
            title (str): The title to validate
        
        Returns:
            str: The validated title
        
        Raises:
            ValueError: If title is invalid
        """
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        return title.strip()

    @staticmethod
    def _validate_price(price):
        """
        Validate price value.
        
        Args:
            price (float): The price to validate
        
        Returns:
            float: The validated price
        
        Raises:
            ValueError: If price is not positive
        """
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number")
        
        if price <= 0:
            raise ValueError("Price must be a positive value")
        
        return price

    @staticmethod
    def _validate_latitude(latitude):
        """
        Validate latitude coordinate.
        
        Args:
            latitude (float): The latitude to validate
        
        Returns:
            float: The validated latitude
        
        Raises:
            ValueError: If latitude is out of range
        """
        try:
            latitude = float(latitude)
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a number")
        
        if not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        
        return latitude

    @staticmethod
    def _validate_longitude(longitude):
        """
        Validate longitude coordinate.
        
        Args:
            longitude (float): The longitude to validate
        
        Returns:
            float: The validated longitude
        
        Raises:
            ValueError: If longitude is out of range
        """
        try:
            longitude = float(longitude)
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a number")
        
        if not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        
        return longitude

    @staticmethod
    def _validate_owner(owner):
        """
        Validate that the owner is a User instance.
        
        Args:
            owner: The owner to validate
        
        Returns:
            User: The validated owner
        
        Raises:
            ValueError: If owner is not a User instance
        """
        from app.models.user import User
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance")
        return owner

    def add_review(self, review):
        """
        Add a review to the place.
        
        Args:
            review (Review): The review to add
        """
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.
        
        Args:
            amenity (Amenity): The amenity to add
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """
        Remove an amenity from the place.
        
        Args:
            amenity (Amenity): The amenity to remove
        """
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def __repr__(self):
        """String representation of the Place."""
        return f"<Place {self.id} - {self.title}>"