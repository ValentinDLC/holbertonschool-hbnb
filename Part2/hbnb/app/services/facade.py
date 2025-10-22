"""
Facade pattern implementation for the HBnB application.
Provides a simplified interface for interacting with the business logic.
"""
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """
    Facade class to handle communication between layers.
    Provides methods for managing users, places, reviews, and amenities.
    """
    
    def __init__(self):
        """Initialize repositories for each entity."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==================== User Management ====================
    
    def create_user(self, user_data):
        """
        Create a new user.
        
        Args:
            user_data (dict): Dictionary containing user information
                - first_name (str): User's first name
                - last_name (str): User's last name
                - email (str): User's email
                - is_admin (bool, optional): Admin status
        
        Returns:
            User: The created user instance
        
        Raises:
            ValueError: If validation fails or email already exists
        """
        # Check if email already exists
        existing_user = self.user_repo.get_by_attribute('email', user_data.get('email'))
        if existing_user:
            raise ValueError("User with this email already exists")
        
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            is_admin=user_data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        
        Args:
            user_id (str): The user's UUID
        
        Returns:
            User: The user instance or None if not found
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email.
        
        Args:
            email (str): The user's email
        
        Returns:
            User: The user instance or None if not found
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Retrieve all users.
        
        Returns:
            list: List of all user instances
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Update a user's information.
        
        Args:
            user_id (str): The user's UUID
            user_data (dict): Dictionary containing fields to update
        
        Returns:
            User: The updated user instance or None if not found
        
        Raises:
            ValueError: If email already exists for another user
        """
        user = self.get_user(user_id)
        if not user:
            return None
        
        # If email is being updated, check it doesn't exist for another user
        if 'email' in user_data:
            existing = self.user_repo.get_by_attribute('email', user_data['email'])
            if existing and existing.id != user_id:
                raise ValueError("Email already exists for another user")
        
        self.user_repo.update(user_id, user_data)
        return user

    def delete_user(self, user_id):
        """
        Delete a user.
        
        Args:
            user_id (str): The user's UUID
        
        Returns:
            bool: True if deleted, False if not found
        """
        user = self.get_user(user_id)
        if user:
            self.user_repo.delete(user_id)
            return True
        return False

    # ==================== Place Management ====================
    
    def create_place(self, place_data):
        """
        Create a new place.
        
        Args:
            place_data (dict): Dictionary containing place information
                - title (str): Place title
                - description (str): Place description
                - price (float): Price per night
                - latitude (float): Latitude coordinate
                - longitude (float): Longitude coordinate
                - owner_id (str): Owner's user ID
        
        Returns:
            Place: The created place instance
        
        Raises:
            ValueError: If validation fails or owner doesn't exist
        """
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")
        
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a place by ID.
        
        Args:
            place_id (str): The place's UUID
        
        Returns:
            Place: The place instance or None if not found
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieve all places.
        
        Returns:
            list: List of all place instances
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update a place's information.
        
        Args:
            place_id (str): The place's UUID
            place_data (dict): Dictionary containing fields to update
        
        Returns:
            Place: The updated place instance or None if not found
        """
        place = self.get_place(place_id)
        if not place:
            return None
        
        self.place_repo.update(place_id, place_data)
        return place

    def delete_place(self, place_id):
        """
        Delete a place.
        
        Args:
            place_id (str): The place's UUID
        
        Returns:
            bool: True if deleted, False if not found
        """
        place = self.get_place(place_id)
        if place:
            self.place_repo.delete(place_id)
            return True
        return False

    # ==================== Review Management ====================
    
    def create_review(self, review_data):
        """
        Create a new review.
        
        Args:
            review_data (dict): Dictionary containing review information
                - text (str): Review content
                - rating (int): Rating (1-5)
                - place_id (str): Place ID being reviewed
                - user_id (str): User ID who wrote the review
        
        Returns:
            Review: The created review instance
        
        Raises:
            ValueError: If validation fails or entities don't exist
        """
        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")
        
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")
        
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,
            user=user
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by ID.
        
        Args:
            review_id (str): The review's UUID
        
        Returns:
            Review: The review instance or None if not found
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.
        
        Returns:
            list: List of all review instances
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.
        
        Args:
            place_id (str): The place's UUID
        
        Returns:
            list: List of review instances for the place
        """
        place = self.get_place(place_id)
        if not place:
            return []
        return place.reviews

    def update_review(self, review_id, review_data):
        """
        Update a review's information.
        
        Args:
            review_id (str): The review's UUID
            review_data (dict): Dictionary containing fields to update
        
        Returns:
            Review: The updated review instance or None if not found
        """
        review = self.get_review(review_id)
        if not review:
            return None
        
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        """
        Delete a review.
        
        Args:
            review_id (str): The review's UUID
        
        Returns:
            bool: True if deleted, False if not found
        """
        review = self.get_review(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False

    # ==================== Amenity Management ====================
    
    def create_amenity(self, amenity_data):
        """
        Create a new amenity.
        
        Args:
            amenity_data (dict): Dictionary containing amenity information
                - name (str): Amenity name
        
        Returns:
            Amenity: The created amenity instance
        
        Raises:
            ValueError: If validation fails or name already exists
        """
        # Check if amenity name already exists
        existing = self.amenity_repo.get_by_attribute('name', amenity_data.get('name'))
        if existing:
            raise ValueError("Amenity with this name already exists")
        
        amenity = Amenity(name=amenity_data.get('name'))
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.
        
        Args:
            amenity_id (str): The amenity's UUID
        
        Returns:
            Amenity: The amenity instance or None if not found
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all amenities.
        
        Returns:
            list: List of all amenity instances
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an amenity's information.
        
        Args:
            amenity_id (str): The amenity's UUID
            amenity_data (dict): Dictionary containing fields to update
        
        Returns:
            Amenity: The updated amenity instance or None if not found
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        
        # If name is being updated, check it doesn't exist
        if 'name' in amenity_data:
            existing = self.amenity_repo.get_by_attribute('name', amenity_data['name'])
            if existing and existing.id != amenity_id:
                raise ValueError("Amenity name already exists")
        
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    def delete_amenity(self, amenity_id):
        """
        Delete an amenity.
        
        Args:
            amenity_id (str): The amenity's UUID
        
        Returns:
            bool: True if deleted, False if not found
        """
        amenity = self.get_amenity(amenity_id)
        if amenity:
            self.amenity_repo.delete(amenity_id)
            return True
        return False

    # ==================== Place-Amenity Relationship ====================
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """
        Add an amenity to a place.
        
        Args:
            place_id (str): The place's UUID
            amenity_id (str): The amenity's UUID
        
        Returns:
            bool: True if added successfully
        
        Raises:
            ValueError: If place or amenity not found
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        
        place.add_amenity(amenity)
        return True

    def remove_amenity_from_place(self, place_id, amenity_id):
        """
        Remove an amenity from a place.
        
        Args:
            place_id (str): The place's UUID
            amenity_id (str): The amenity's UUID
        
        Returns:
            bool: True if removed successfully
        
        Raises:
            ValueError: If place or amenity not found
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        
        place.remove_amenity(amenity)
        return True