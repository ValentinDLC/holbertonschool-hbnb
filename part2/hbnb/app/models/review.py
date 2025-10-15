from base_model import BaseModel
from place import Place
from user import User

class Review(BaseModel):
    """
    """
    MIN_RATING = 1
    MAX_RATING = 5
    def __init__(self, text, rating, place, user):
        """
        Initialize a Review instance.

        Args:
            text (str):
            rating (int): 
            place (Place)
            user (User)
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def validate_text(text):
        """
        """
        if not isinstance(text, str):
            raise ValueError("")
        
    def validate_rating(rating):
        """
        """
        if not isinstance(rating, int) or rating < MIN_RATING or rating > MAX_RATING:
            raise ValueError("Rating must be an integer between 1 and 5")
        
    def validate_place(place):
        """
        Check if place is a Place instance.
        """
        if not isinstance(place, Place):
            raise ValueError("place must be a valid instance of Place")
        
    def validate_user(user):
        """
        Check if user is a User instance.
        """
        if not isinstance(user, User):
            raise ValueError("user must be a valid instance of User")