"""
User model for the HBnB application.
Represents a user who can own places and write reviews.
"""
from app.models.base_model import BaseModel
import re


class User(BaseModel):
    """User class representing a user in the system."""
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a User instance.
        
        Args:
            first_name (str): User's first name (max 50 characters)
            last_name (str): User's last name (max 50 characters)
            email (str): User's email address (must be unique and valid)
            is_admin (bool): Whether the user has admin privileges (default: False)
        
        Raises:
            ValueError: If validation fails for any attribute
        """
        super().__init__()
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.places = []  # List to store places owned by the user
        self.reviews = []  # List to store reviews written by the user

    @staticmethod
    def _validate_name(name, field_name):
        """
        Validate name fields.
        
        Args:
            name (str): The name to validate
            field_name (str): The name of the field for error messages
        
        Returns:
            str: The validated name
        
        Raises:
            ValueError: If name is empty or exceeds 50 characters
        """
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        if len(name) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        return name.strip()

    @staticmethod
    def _validate_email(email):
        """
        Validate email format.
        
        Args:
            email (str): The email to validate
        
        Returns:
            str: The validated email
        
        Raises:
            ValueError: If email format is invalid
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        # Basic email validation regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        
        return email.lower().strip()

    def add_place(self, place):
        """
        Add a place to the user's list of owned places.
        
        Args:
            place: The Place instance to add
        """
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """
        Add a review to the user's list of reviews.
        
        Args:
            review: The Review instance to add
        """
        if review not in self.reviews:
            self.reviews.append(review)

    def __repr__(self):
        """String representation of the User."""
        return f"<User {self.id} - {self.first_name} {self.last_name}>"