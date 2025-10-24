"""
Test file for validating the core business logic classes.
Run this file to test the implementation of User, Place, Review, and Amenity.
"""
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user_creation():
    """Test creating a User instance."""
    print("Testing User creation...")
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    assert len(user.id) > 0
    assert user.created_at is not None
    assert user.updated_at is not None
    print("✓ User creation test passed!")


def test_user_validation():
    """Test User validation."""
    print("\nTesting User validation...")
    
    # Test invalid first name
    try:
        User(first_name="", last_name="Doe", email="test@example.com")
        assert False, "Should raise ValueError for empty first name"
    except ValueError:
        print("✓ Empty first name validation passed")
    
    # Test invalid email
    try:
        User(first_name="John", last_name="Doe", email="invalid-email")
        assert False, "Should raise ValueError for invalid email"
    except ValueError:
        print("✓ Invalid email validation passed")
    
    # Test name too long
    try:
        User(first_name="A" * 51, last_name="Doe", email="test@example.com")
        assert False, "Should raise ValueError for name too long"
    except ValueError:
        print("✓ Name length validation passed")


def test_place_creation():
    """Test creating a Place instance."""
    print("\nTesting Place creation...")
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    assert place.title == "Cozy Apartment"
    assert place.description == "A nice place to stay"
    assert place.price == 100.0
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner == owner
    assert place in owner.places
    print("✓ Place creation test passed!")


def test_place_validation():
    """Test Place validation."""
    print("\nTesting Place validation...")
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    
    # Test invalid price
    try:
        Place(
            title="Test",
            description="Test",
            price=-100,
            latitude=0,
            longitude=0,
            owner=owner
        )
        assert False, "Should raise ValueError for negative price"
    except ValueError:
        print("✓ Negative price validation passed")
    
    # Test invalid latitude
    try:
        Place(
            title="Test",
            description="Test",
            price=100,
            latitude=91,
            longitude=0,
            owner=owner
        )
        assert False, "Should raise ValueError for invalid latitude"
    except ValueError:
        print("✓ Latitude range validation passed")
    
    # Test invalid longitude
    try:
        Place(
            title="Test",
            description="Test",
            price=100,
            latitude=0,
            longitude=181,
            owner=owner
        )
        assert False, "Should raise ValueError for invalid longitude"
    except ValueError:
        print("✓ Longitude range validation passed")


def test_review_creation():
    """Test creating a Review instance with relationships."""
    print("\nTesting Review creation...")
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    reviewer = User(first_name="Bob", last_name="Jones", email="bob@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    review = Review(
        text="Great stay!",
        rating=5,
        place=place,
        user=reviewer
    )
    
    assert review.text == "Great stay!"
    assert review.rating == 5
    assert review.place == place
    assert review.user == reviewer
    assert review in place.reviews
    assert review in reviewer.reviews
    print("✓ Review creation and relationships test passed!")


def test_review_validation():
    """Test Review validation."""
    print("\nTesting Review validation...")
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    reviewer = User(first_name="Bob", last_name="Jones", email="bob@example.com")
    place = Place(
        title="Test",
        description="Test",
        price=100,
        latitude=0,
        longitude=0,
        owner=owner
    )
    
    # Test invalid rating
    try:
        Review(text="Test", rating=6, place=place, user=reviewer)
        assert False, "Should raise ValueError for rating > 5"
    except ValueError:
        print("✓ Rating range validation passed")
    
    # Test empty text
    try:
        Review(text="", rating=5, place=place, user=reviewer)
        assert False, "Should raise ValueError for empty text"
    except ValueError:
        print("✓ Empty text validation passed")


def test_amenity_creation():
    """Test creating an Amenity instance."""
    print("\nTesting Amenity creation...")
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert len(amenity.id) > 0
    print("✓ Amenity creation test passed!")


def test_amenity_validation():
    """Test Amenity validation."""
    print("\nTesting Amenity validation...")
    
    # Test name too long
    try:
        Amenity(name="A" * 51)
        assert False, "Should raise ValueError for name too long"
    except ValueError:
        print("✓ Amenity name length validation passed")
    
    # Test empty name
    try:
        Amenity(name="")
        assert False, "Should raise ValueError for empty name"
    except ValueError:
        print("✓ Empty name validation passed")


def test_place_amenity_relationship():
    """Test many-to-many relationship between Place and Amenity."""
    print("\nTesting Place-Amenity relationship...")
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Test Place",
        description="Test",
        price=100,
        latitude=0,
        longitude=0,
        owner=owner
    )
    
    wifi = Amenity(name="Wi-Fi")
    parking = Amenity(name="Parking")
    
    place.add_amenity(wifi)
    place.add_amenity(parking)
    
    assert len(place.amenities) == 2
    assert wifi in place.amenities
    assert parking in place.amenities
    print("✓ Place-Amenity relationship test passed!")


def test_update_method():
    """Test the update method."""
    print("\nTesting update method...")
    user = User(first_name="John", last_name="Doe", email="john@example.com")
    
    original_updated_at = user.updated_at
    import time
    time.sleep(0.01)  # Small delay to ensure timestamp changes
    
    user.update({"first_name": "Jane"})
    
    assert user.first_name == "Jane"
    assert user.updated_at > original_updated_at
    print("✓ Update method test passed!")


def run_all_tests():
    """Run all test functions."""
    print("=" * 50)
    print("Running Core Business Logic Tests")
    print("=" * 50)
    
    test_user_creation()
    test_user_validation()
    test_place_creation()
    test_place_validation()
    test_review_creation()
    test_review_validation()
    test_amenity_creation()
    test_amenity_validation()
    test_place_amenity_relationship()
    test_update_method()
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()