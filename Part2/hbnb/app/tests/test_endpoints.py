"""
Comprehensive unit tests for all HBnB API endpoints.
Tests validation, CRUD operations, and error handling.
"""
import unittest
import json
import uuid
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User endpoints"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.base_url = '/api/v1/users/'
        
        # Use unique identifier for each test
        self.unique_id = str(uuid.uuid4())[:8]
    
    def tearDown(self):
        """Clean up after each test"""
        pass
    
    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post(self.base_url, json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.{self.unique_id}@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertIn('@example.com', data['email'])
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email format"""
        response = self.client.post(self.base_url, json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('email', data['error'].lower())
    
    def test_create_user_empty_first_name(self):
        """Test user creation with empty first name"""
        response = self.client.post(self.base_url, json={
            "first_name": "",
            "last_name": "Doe",
            "email": f"test.{self.unique_id}@example.com"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_user_empty_last_name(self):
        """Test user creation with empty last name"""
        response = self.client.post(self.base_url, json={
            "first_name": "John",
            "last_name": "",
            "email": f"test.{self.unique_id}@example.com"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email"""
        email = f"duplicate.{self.unique_id}@example.com"
        
        # Create first user
        response1 = self.client.post(self.base_url, json={
            "first_name": "First",
            "last_name": "User",
            "email": email
        })
        self.assertEqual(response1.status_code, 201)
        
        # Try to create second user with same email
        response2 = self.client.post(self.base_url, json={
            "first_name": "Second",
            "last_name": "User",
            "email": email
        })
        self.assertEqual(response2.status_code, 400)
        data = json.loads(response2.data)
        self.assertIn('error', data)
        self.assertIn('already', data['error'].lower())
    
    def test_get_user_success(self):
        """Test successful user retrieval by ID"""
        # Create user first
        create_response = self.client.post(self.base_url, json={
            "first_name": "Test",
            "last_name": "User",
            "email": f"test.get.{self.unique_id}@example.com"
        })
        user_id = json.loads(create_response.data)['id']
        
        # Get user
        response = self.client.get(f"{self.base_url}{user_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['first_name'], 'Test')
    
    def test_get_user_not_found(self):
        """Test retrieving non-existent user returns 404"""
        response = self.client.get(f"{self.base_url}fake-id-12345")
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('not found', data['error'].lower())
    
    def test_get_all_users(self):
        """Test retrieving all users"""
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_update_user_success(self):
        """Test successful user update"""
        # Create user
        create_response = self.client.post(self.base_url, json={
            "first_name": "Original",
            "last_name": "Name",
            "email": f"original.{self.unique_id}@example.com"
        })
        user_id = json.loads(create_response.data)['id']
        
        # Update user
        response = self.client.put(f"{self.base_url}{user_id}", json={
            "first_name": "Updated",
            "last_name": "Name",
            "email": f"updated.{self.unique_id}@example.com"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')
    
    def test_update_user_not_found(self):
        """Test updating non-existent user returns 404"""
        response = self.client.put(f"{self.base_url}fake-id-12345", json={
            "first_name": "Test",
            "last_name": "User",
            "email": f"test.{self.unique_id}@example.com"
        })
        self.assertEqual(response.status_code, 404)


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity endpoints"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.base_url = '/api/v1/amenities/'
        
        self.unique_id = str(uuid.uuid4())[:8]
    
    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post(self.base_url, json={
            "name": f"Test WiFi {self.unique_id}"
        })
        self.assertIn(response.status_code, [200, 201])
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertIn('WiFi', data['name'])
    
    def test_create_amenity_empty_name(self):
        """Test amenity creation with empty name"""
        response = self.client.post(self.base_url, json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_amenity_name_too_long(self):
        """Test amenity creation with name exceeding max length"""
        response = self.client.post(self.base_url, json={
            "name": "A" * 51  # Max is 50
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_amenity_duplicate_name(self):
        """Test creating duplicate amenity"""
        name = f"Duplicate Amenity {self.unique_id}"
        
        # Create first amenity
        response1 = self.client.post(self.base_url, json={"name": name})
        self.assertIn(response1.status_code, [200, 201])
        
        # Try to create duplicate
        response2 = self.client.post(self.base_url, json={"name": name})
        self.assertEqual(response2.status_code, 409)
        data = json.loads(response2.data)
        self.assertIn('error', data)
        self.assertIn('already exists', data['error'].lower())
    
    def test_get_amenity_success(self):
        """Test successful amenity retrieval"""
        # Create amenity
        create_response = self.client.post(self.base_url, json={
            "name": f"Test Amenity {self.unique_id}"
        })
        amenity_id = json.loads(create_response.data)['id']
        
        # Get amenity
        response = self.client.get(f"{self.base_url}{amenity_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], amenity_id)
    
    def test_get_amenity_not_found(self):
        """Test retrieving non-existent amenity"""
        response = self.client.get(f"{self.base_url}fake-id-12345")
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_update_amenity_success(self):
        """Test successful amenity update"""
        # Create amenity
        create_response = self.client.post(self.base_url, json={
            "name": f"Original Amenity {self.unique_id}"
        })
        amenity_id = json.loads(create_response.data)['id']
        
        # Update amenity
        response = self.client.put(f"{self.base_url}{amenity_id}", json={
            "name": f"Updated Amenity {self.unique_id}"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Updated', data['name'])
    
    def test_update_amenity_not_found(self):
        """Test updating non-existent amenity"""
        response = self.client.put(f"{self.base_url}fake-id-12345", json={
            "name": "Test"
        })
        self.assertEqual(response.status_code, 404)


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place endpoints"""
    
    def setUp(self):
        """Set up test client and create owner"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.base_url = '/api/v1/places/'
        
        self.unique_id = str(uuid.uuid4())[:8]
        
        # Create owner for place tests with unique email
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": f"owner.place.{self.unique_id}@example.com"
        })
        
        # Debug et vérification
        if owner_response.status_code != 201:
            print(f"\n=== ERREUR dans TestPlaceEndpoints.setUp ===")
            print(f"Status: {owner_response.status_code}")
            print(f"Data: {owner_response.data}")
            self.fail(f"Échec création owner: {owner_response.data}")
        
        response_data = json.loads(owner_response.data)
        if 'id' not in response_data:
            self.fail(f"Pas de champ 'id' dans la réponse: {response_data}")
            
        self.owner_id = response_data['id']
    
    def test_create_place_success(self):
        """Test successful place creation"""
        response = self.client.post(self.base_url, json={
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Test Place')
        self.assertEqual(data['price'], 100.0)
    
    def test_create_place_empty_title(self):
        """Test place creation with empty title"""
        response = self.client.post(self.base_url, json={
            "title": "",
            "price": 100.0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_place_negative_price(self):
        """Test place creation with negative price"""
        response = self.client.post(self.base_url, json={
            "title": "Test Place",
            "price": -50.0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('price', data['error'].lower())
    
    def test_create_place_zero_price(self):
        """Test place creation with zero price"""
        response = self.client.post(self.base_url, json={
            "title": "Test Place",
            "price": 0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_place_invalid_latitude_high(self):
        """Test place creation with latitude > 90"""
        response = self.client.post(self.base_url, json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 91,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('latitude', data['error'].lower())
    
    def test_create_place_invalid_latitude_low(self):
        """Test place creation with latitude < -90"""
        response = self.client.post(self.base_url, json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": -91,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_place_invalid_longitude_high(self):
        """Test place creation with longitude > 180"""
        response = self.client.post(self.base_url, json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 0,
            "longitude": 181,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('longitude', data['error'].lower())
    
    def test_create_place_invalid_longitude_low(self):
        """Test place creation with longitude < -180"""
        response = self.client.post(self.base_url, json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 0,
            "longitude": -181,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_place_nonexistent_owner(self):
        """Test place creation with non-existent owner"""
        response = self.client.post(self.base_url, json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": "fake-owner-id-12345"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_place_success(self):
        """Test successful place retrieval"""
        # Create place
        create_response = self.client.post(self.base_url, json={
            "title": "Get Test Place",
            "price": 100.0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        place_id = json.loads(create_response.data)['id']
        
        # Get place
        response = self.client.get(f"{self.base_url}{place_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('owner', data)
        self.assertIn('amenities', data)
    
    def test_get_place_not_found(self):
        """Test retrieving non-existent place"""
        response = self.client.get(f"{self.base_url}fake-id-12345")
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_places(self):
        """Test retrieving all places"""
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_update_place_success(self):
        """Test successful place update"""
        # Create place
        create_response = self.client.post(self.base_url, json={
            "title": "Original Place",
            "price": 100.0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        place_id = json.loads(create_response.data)['id']
        
        # Update place
        response = self.client.put(f"{self.base_url}{place_id}", json={
            "title": "Updated Place",
            "price": 150.0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Place')
        self.assertEqual(data['price'], 150.0)


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review endpoints"""
    
    def setUp(self):
        """Set up test client and create user and place"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.base_url = '/api/v1/reviews/'
        
        self.unique_id = str(uuid.uuid4())[:8]
        
        # Create owner
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Review",
            "email": f"owner.review.{self.unique_id}@example.com"
        })
        
        if owner_response.status_code != 201:
            self.fail(f"Échec création owner: {owner_response.data}")
        
        owner_id = json.loads(owner_response.data)['id']
        
        # Create reviewer
        reviewer_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "Test",
            "email": f"reviewer.test.{self.unique_id}@example.com"
        })
        
        if reviewer_response.status_code != 201:
            self.fail(f"Échec création reviewer: {reviewer_response.data}")
        
        self.reviewer_id = json.loads(reviewer_response.data)['id']
        
        # Create place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Review Place",
            "price": 100.0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": owner_id
        })
        
        if place_response.status_code != 201:
            self.fail(f"Échec création place: {place_response.data}")
        
        self.place_id = json.loads(place_response.data)['id']
    
    def test_create_review_success(self):
        """Test successful review creation"""
        response = self.client.post(self.base_url, json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['text'], 'Great place!')
    
    def test_create_review_empty_text(self):
        """Test review creation with empty text"""
        response = self.client.post(self.base_url, json={
            "text": "",
            "rating": 5,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('text', data['error'].lower())
    
    def test_create_review_invalid_rating_high(self):
        """Test review creation with rating > 5"""
        response = self.client.post(self.base_url, json={
            "text": "Test review",
            "rating": 6,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('rating', data['error'].lower())
    
    def test_create_review_invalid_rating_low(self):
        """Test review creation with rating < 1"""
        response = self.client.post(self.base_url, json={
            "text": "Test review",
            "rating": 0,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_review_nonexistent_user(self):
        """Test review creation with non-existent user"""
        response = self.client.post(self.base_url, json={
            "text": "Test review",
            "rating": 5,
            "user_id": "fake-user-id-12345",
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_review_nonexistent_place(self):
        """Test review creation with non-existent place"""
        response = self.client.post(self.base_url, json={
            "text": "Test review",
            "rating": 5,
            "user_id": self.reviewer_id,
            "place_id": "fake-place-id-12345"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_review_success(self):
        """Test successful review retrieval"""
        # Create review
        create_response = self.client.post(self.base_url, json={
            "text": "Test review",
            "rating": 4,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        })
        review_id = json.loads(create_response.data)['id']
        
        # Get review
        response = self.client.get(f"{self.base_url}{review_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], review_id)
    
    def test_get_review_not_found(self):
        """Test retrieving non-existent review"""
        response = self.client.get(f"{self.base_url}fake-id-12345")
        self.assertEqual(response.status_code, 404)
    
    def test_delete_review_success(self):
        """Test successful review deletion"""
        # Create review
        create_response = self.client.post(self.base_url, json={
            "text": "To be deleted",
            "rating": 3,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        })
        review_id = json.loads(create_response.data)['id']
        
        # Delete review
        response = self.client.delete(f"{self.base_url}{review_id}")
        self.assertEqual(response.status_code, 200)
        
        # Verify deletion
        get_response = self.client.get(f"{self.base_url}{review_id}")
        self.assertEqual(get_response.status_code, 404)
    
    def test_delete_review_not_found(self):
        """Test deleting non-existent review"""
        response = self.client.delete(f"{self.base_url}fake-id-12345")
        self.assertEqual(response.status_code, 404)


class TestBoundaryValues(unittest.TestCase):
    """Test cases for boundary value validation"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app()
        self.client = self.app.test_client()
        
        self.unique_id = str(uuid.uuid4())[:8]
        
        # Create owner for boundary tests
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": f"boundary.owner.{self.unique_id}@example.com"
        })
        
        if owner_response.status_code != 201:
            self.fail(f"Échec création owner: {owner_response.data}")
        
        self.owner_id = json.loads(owner_response.data)['id']
    
    def test_latitude_boundaries(self):
        """Test latitude boundary values"""
        # Valid boundaries
        valid_latitudes = [-90, -45, 0, 45, 90]
        for lat in valid_latitudes:
            response = self.client.post('/api/v1/places/', json={
                "title": f"Place {lat} {uuid.uuid4()}",
                "price": 100.0,
                "latitude": lat,
                "longitude": 0,
                "owner_id": self.owner_id
            })
            self.assertEqual(response.status_code, 201,
                           f"Latitude {lat} should be valid")
        
        # Invalid boundaries
        invalid_latitudes = [-91, 91, -100, 100]
        for lat in invalid_latitudes:
            response = self.client.post('/api/v1/places/', json={
                "title": f"Place {lat} {uuid.uuid4()}",
                "price": 100.0,
                "latitude": lat,
                "longitude": 0,
                "owner_id": self.owner_id
            })
            self.assertEqual(response.status_code, 400,
                           f"Latitude {lat} should be invalid")
    
    def test_longitude_boundaries(self):
        """Test longitude boundary values"""
        # Valid boundaries
        valid_longitudes = [-180, -90, 0, 90, 180]
        for lon in valid_longitudes:
            response = self.client.post('/api/v1/places/', json={
                "title": f"Place {lon} {uuid.uuid4()}",
                "price": 100.0,
                "latitude": 0,
                "longitude": lon,
                "owner_id": self.owner_id
            })
            self.assertEqual(response.status_code, 201,
                           f"Longitude {lon} should be valid")
        
        # Invalid boundaries
        invalid_longitudes = [-181, 181, -200, 200]
        for lon in invalid_longitudes:
            response = self.client.post('/api/v1/places/', json={
                "title": f"Place {lon} {uuid.uuid4()}",
                "price": 100.0,
                "latitude": 0,
                "longitude": lon,
                "owner_id": self.owner_id
            })
            self.assertEqual(response.status_code, 400,
                           f"Longitude {lon} should be invalid")
    
    def test_rating_boundaries(self):
        """Test rating boundary values"""
        # Create place and reviewer
        place_response = self.client.post('/api/v1/places/', json={
            "title": f"Test Place {uuid.uuid4()}",
            "price": 100.0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        
        if place_response.status_code != 201:
            self.fail(f"Échec création place: {place_response.data}")
        
        place_id = json.loads(place_response.data)['id']
        
        reviewer_response = self.client.post('/api/v1/users/', json={   \
            "first_name": "Reviewer",
            "last_name": "Boundary",
            "email": f"reviewer.boundary.{self.unique_id}@example.com"
        })
        
        if reviewer_response.status_code != 201:
            self.fail(f"Échec création reviewer: {reviewer_response.data}")
        
        reviewer_id = json.loads(reviewer_response.data)['id']
        
        # Valid ratings
        valid_ratings = [1, 2, 3, 4, 5]
        for rating in valid_ratings:
            response = self.client.post('/api/v1/reviews/', json={
                "text": "Valid rating test",
                "rating": rating,
                "user_id": reviewer_id,
                "place_id": place_id
            })
            self.assertEqual(response.status_code, 201,
                             f"Rating {rating} should be valid")
        
        # Invalid ratings
        invalid_ratings = [0, 6, -1]
        for rating in invalid_ratings:
            response = self.client.post('/api/v1/reviews/', json={
                "text": "Invalid rating test",
                "rating": rating,
                "user_id": reviewer_id,
                "place_id": place_id
            })
            self.assertEqual(response.status_code, 400,
                             f"Rating {rating} should be invalid")

if __name__ == '__main__':
    unittest.main()
