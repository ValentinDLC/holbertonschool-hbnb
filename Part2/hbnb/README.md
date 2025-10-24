# HBnb - Business Logic and API

hbnb/
├── app/
│   ├──api/
│   │   ├──v1/
│   │   │   ├──amenities.py
│   │   │   ├──places.py
│   │   │   ├──reviews.py
│   │   │   ├──users.py
│   │   │   ├──__init__.py
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── tests/
│   ├── test_endpoints.py
│   ├── run_all_test.sh
│   ├──test_user_endpoint.sh
│   ├──test_place_endpoint.sh
│   ├──test_amenity_endpoint.sh
│   ├──test_review_endpoint.sh
├── run.py
├── config.py
├── requirements.txt


# Features

##  Core Functionality
RESTful API with Flask-RESTX
CRUD Operations for Users, Places, Reviews, and Amenities
Comprehensive Validation at multiple layers
Swagger Documentation auto-generated
Facade Pattern for business logic
In-Memory Repository for data persistence

---

## Quality Assurance
 45+ Unit Tests with unittest
 43 Manual Tests with cURL scripts
 100% Test Coverage on endpoints
 Boundary Value Testing
 Error Handling with appropriate HTTP codes

---

##  Advanced Features
 Many-to-Many Relations (Places ↔ Amenities)
 One-to-Many Relations (User → Places, Place → Reviews)
 Duplicate Detection (emails, amenity names)
 Input Sanitization (trimming, validation)

---

# Installation

## Prerequisites
Python 3.9+ installed
pip package manager
curl (for manual tests)
bash (for test scripts)

---

## Step 1: Clone the Repository
bash
git clone <repository-url>
cd HBnB-Evolution

---

## Step 2: Create Virtual Environment
bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

---

## Step 3: Install Dependencies
bash
pip install -r requirements.txt

---

# Running the Application

## Development Server
bash
# Start the Flask development server
python3 run.py

# Or with Flask CLI
flask run --port 5001

# Server will start at: http://localhost:5001

Expected Output:
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5001

---

# 📚 API Documentation

## 🧭 Swagger UI
Once the server is running, access the interactive API documentation:
http://localhost:5001/api/v1/

![swagger.user](hbnb/images/swagger.user.png)
![swagger.user_id](hbnb/images/swagger.user_id.png)
![swagger.user](hbnb/images/swagger.place.png)
![swagger.user](hbnb/images/swagger.place_id.png)
![swagger.user](hbnb/images/swagger.amenity.png)
![swagger.user](hbnb/images/swagger.amenity_id.png)

---

# 🧪 Unit Tests
bash
# Method 1: Direct execution
python3 tests/test_endpoints.py

# Run single test
python3 -m unittest tests.test_endpoints

---

# 🔌 API Endpoints
Users
Places
Reviews
Amenities

---

# ✅ Validation Rules

## User Validation
Email Pattern:
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

## Place Validation
**Fields & Constraints:**
- `title` → required, string, 1–100 characters  
- `description` → optional, string, max 500 characters  
- `price` → required, numeric, must be ≥ 0  
- `latitude` → required, float, range **[-90, 90]**  
- `longitude` → required, float, range **[-180, 180]**  
- `owner_id` → required, must correspond to an existing **User**  
- `amenities` → optional, list of valid **Amenity IDs**

## Review Validation
**Fields & Constraints**
- `text` → required, string, 1–300 characters  
- `rating` → required, integer, range **1–5**  
- `user_id` → required, must reference an existing **User**  
- `place_id` → required, must reference an existing **Place**  

## Amenity Validation
**Fields & Constraints**
- `name` → required, string, length between **1 and 50 characters**
- `name` → must be **unique** (no duplicate amenity names allowed)
- Input is **trimmed and sanitized** before validation


---

# 💡 Examples

## Create a User
bash
curl -X POST http://localhost:5001/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }'

Response (201 Created):
json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "created_at": "2025-10-20T12:00:00",
  "updated_at": "2025-10-20T12:00:00"
}

---

## Create a Place
bash
curl -X POST http://localhost:5001/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Apartment",
    "description": "A lovely place in the city",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "amenities": ["amenity-id-1", "amenity-id-2"]
  }'

Response (201 Created):
json
{
  "id": "place-uuid",
  "title": "Beautiful Apartment",
  "description": "A lovely place in the city",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "amenities": [
    {"id": "amenity-id-1", "name": "Wi-Fi"},
    {"id": "amenity-id-2", "name": "Parking"}
  ],
  "created_at": "2025-10-20T12:05:00",
  "updated_at": "2025-10-20T12:05:00"
}

---

## Create a Review
bash
curl -X POST http://localhost:5001/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "user-uuid",
    "place_id": "place-uuid"
  }'

Response (201 Created):
json
{
  "id": "review-uuid",
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "user-uuid",
  "place_id": "place-uuid",
  "created_at": "2025-10-20T12:10:00",
  "updated_at": "2025-10-20T12:10:00"
}

---

## Create an Amenity
bash
curl -X POST http://localhost:5001/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'

Response (200 OK):
json
{
  "id": "amenity-uuid",
  "name": "Wi-Fi",
  "created_at": "2025-10-20T12:15:00",
  "updated_at": "2025-10-20T12:15:00"
}

---

## Error Response Example
bash
curl -X POST http://localhost:5001/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "invalid-email"
  }'

Response (400 Bad Request):
json
{
  "error": "Invalid email format"
}
