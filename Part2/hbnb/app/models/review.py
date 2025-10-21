"""
Review model for the HBnB application.
Represents a review written by a user for a place.
"""
from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review class representing a user's review of a place."""
    def __init__(self, text, rating, place, user):
        """
        Initialize a Review instance.
        
        Args:
            text (str): The content of the review (required)
            rating (int): Rating value (1-5)
            place (Place): The place being reviewed
            user (User): The user who wrote the review
        
        Raises:
            ValueError: If validation fails for any attribute
        """
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = self._validate_place(place)
        self.user = self._validate_user(user)

        if hasattr(place, 'add_review'):
            place.add_review(self)
        if hasattr(user, 'add_review'):
            user.add_review(self)

    @staticmethod
    def _validate_text(text):
        """
        Validate review text.
        
        Args:
            text (str): The review text to validate
        
        Returns:
            str: The validated text
        
        Raises:
            ValueError: If text is empty
        """
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        return text.strip()
    @staticmethod
    def _validate_rating(rating):
        """
        Validate rating value.
        
        Args:
            rating (int): The rating to validate
        
        Returns:
            int: The validated rating
        
        Raises:
            ValueError: If rating is not between 1 and 5
        """
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer")
        
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        return rating
    @staticmethod
    def _validate_place(place):
        """
        Validate that the place is a Place instance.
        
        Args:
            place: The place to validate
        
        Returns:
            Place: The validated place
        
        Raises:
            ValueError: If place is not a Place instance
        """
        from app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("Place must be a valid place instance")
        return place
    
    @staticmethod
    def _validate_user(user):
        """
        Validate that the user is a User instance.
        
        Args:
            user: The user to validate
        
        Returns:
            User: The validated user
        
        Raises:
            ValueError: If user is not a User instance
        """
        from app.models.user import User
        if not isinstance(user, User):
            raise ValueError("User must be a valid user instance")
        return user 
    
    def __repr__(self):
        """String representation of the Review."""
        return f"<Review {self.id} - Rating: {self.rating}>"

