# HBnb - Business Logic and API

## Fichier: README.md

```markdown
# HBnB Application - Part 2

## Project Overview

This is the implementation of Part 2 of the HBnB project, focusing on building the Presentation and Business Logic layers using Python and Flask.

## Project Structure

- **app/**: Core application code
  - **api/**: API endpoints organized by version
    - **v1/**: Version 1 of the API
      - `users.py`: User-related endpoints
      - `places.py`: Place-related endpoints
      - `reviews.py`: Review-related endpoints
      - `amenities.py`: Amenity-related endpoints
  - **models/**: Business logic classes
    - `user.py`: User model
    - `place.py`: Place model
    - `review.py`: Review model
    - `amenity.py`: Amenity model
  - **services/**: Facade pattern implementation
    - `facade.py`: HBnBFacade class for layer communication
  - **persistence/**: Data persistence layer
    - `repository.py`: In-memory repository implementation

- **run.py**: Application entry point
- **config.py**: Configuration settings
- **requirements.txt**: Python dependencies
- **README.md**: Project documentation

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python run.py
```

The application will run on `http://localhost:5000` with debug mode enabled.

## API Documentation

Once the application is running, access the interactive API documentation at:
`http://localhost:5001/api/v1/`

## Development Status

**Current Phase**: Task 0 - Project Setup and Package Initialization

**Implemented**:
- Project structure with modular architecture
- In-memory repository for object storage
- Facade pattern for layer communication
- Flask application with flask-restx

**To Be Implemented**:
- Business logic models (User, Place, Review, Amenity)
- API endpoints for CRUD operations
- Data validation and serialization
- JWT authentication (Part 3)
- Database persistence with SQLAlchemy (Part 3)

## Notes

- The current implementation uses an in-memory repository for data storage
- This will be replaced with a database-backed solution in Part 3
- Authentication and authorization will be added in Part 3
```

## Fichiers __init__.py vides

Créez des fichiers `__init__.py` vides dans les répertoires suivants:
- `app/persistence/__init__.py`
- `app/models/__init__.py`
- `app/api/__init__.py`
- `app/api/v1/__init__.py`

## Fichiers de modèles vides (à implémenter plus tard)

Créez des fichiers vides pour les modèles:
- `app/models/user.py`
- `app/models/place.py`
- `app/models/review.py`
- `app/models/amenity.py`

## Fichiers d'endpoints vides (à implémenter plus tard)

Créez des fichiers vides pour les endpoints:
- `app/api/v1/users.py`
- `app/api/v1/places.py`
- `app/api/v1/reviews.py`
- `app/api/v1/amenities.py`

## Instructions de déploiement

1. Créez les dossiers selon la structure indiquée
2. Copiez le contenu de chaque section dans les fichiers correspondants
3. Créez les fichiers `__init__.py` vides où nécessaire
4. Installez les dépendances: `pip install -r requirements.txt`
5. Lancez l'application: `python run.py`

Le projet est maintenant prêt pour l'implémentation des modèles et des endpoints dans les tâches suivantes!




```markdown
# HBnB Application - Part 2

## Project Overview

This is the implementation of Part 2 of the HBnB project, focusing on building the Presentation and Business Logic layers using Python and Flask.

## Project Structure

- **app/**: Core application code
  - **api/**: API endpoints organized by version
    - **v1/**: Version 1 of the API
  - **models/**: Business logic classes
    - `base_model.py`: Base class with common attributes
    - `user.py`: User model
    - `place.py`: Place model
    - `review.py`: Review model
    - `amenity.py`: Amenity model
  - **services/**: Facade pattern implementation
    - `facade.py`: HBnBFacade class for layer communication
  - **persistence/**: Data persistence layer
    - `repository.py`: In-memory repository implementation

- **tests/**: Test files
  - `test_models.py`: Tests for business logic classes

## Business Logic Layer

### Entities and Relationships

#### User
Represents a user in the system who can own places and write reviews.

**Attributes:**
- `id` (str): Unique UUID identifier
- `first_name` (str): First name (max 50 characters)
- `last_name` (str): Last name (max 50 characters)
- `email` (str): Email address (unique, validated format)
- `is_admin` (bool): Admin privileges flag (default: False)
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Relationships:**
- One-to-many with Place (can own multiple places)
- One-to-many with Review (can write multiple reviews)

#### Place
Represents a rentable property in the system.

**Attributes:**
- `id` (str): Unique UUID identifier
- `title` (str): Place title (max 100 characters)
- `description` (str): Detailed description (optional)
- `price` (float): Price per night (must be positive)
- `latitude` (float): Latitude coordinate (-90.0 to 90.0)
- `longitude` (float): Longitude coordinate (-180.0 to 180.0)
- `owner` (User): Owner of the place
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Relationships:**
- Many-to-one with User (has one owner)
- One-to-many with Review (can have multiple reviews)
- Many-to-many with Amenity (can have multiple amenities)

#### Review
Represents a review written by a user for a place.

**Attributes:**
- `id` (str): Unique UUID identifier
- `text` (str): Review content (required)
- `rating` (int): Rating value (1-5)
- `place` (Place): Place being reviewed
- `user` (User): User who wrote the review
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Relationships:**
- Many-to-one with Place (reviews one place)
- Many-to-one with User (written by one user)

#### Amenity
Represents a feature or service available at places.

**Attributes:**
- `id` (str): Unique UUID identifier
- `name` (str): Amenity name (max 50 characters)
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Relationships:**
- Many-to-many with Place (can be associated with multiple places)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python run.py
```

The application will run on `http://localhost:5000` with debug mode enabled.

## Running Tests

To test the business logic implementation:

```bash
python tests/test_models.py
```

This will run comprehensive tests for all models including:
- Entity creation
- Attribute validation
- Relationship handling
- Update functionality

## API Documentation

Once the application is running, access the interactive API documentation at:
`http://localhost:5000/api/v1/`

## Development Status

**Current Phase**: Task 1 - Core Business Logic Classes ✓

**Completed:**
- ✓ Project structure with modular architecture
- ✓ In-memory repository for object storage
- ✓ Facade pattern for layer communication
- ✓ Flask application with flask-restx
- ✓ BaseModel with UUID and timestamp management
- ✓ User model with validation
- ✓ Place model with validation and relationships
- ✓ Review model with validation and relationships
- ✓ Amenity model with validation
- ✓ Comprehensive test suite

**To Be Implemented:**
- API endpoints for CRUD operations
- Data serialization for API responses
- JWT authentication (Part 3)
- Database persistence with SQLAlchemy (Part 3)

## Usage Examples

### Creating a User

```python
from app.models.user import User

user = User(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com"
)
```

### Creating a Place

```python
from app.models.place import Place

place = Place(
    title="Cozy Apartment",
    description="A beautiful place to stay",
    price=100.0,
    latitude=37.7749,
    longitude=-122.4194,
    owner=user
)
```

### Adding a Review

```python
from app.models.review import Review

review = Review(
    text="Great stay! Highly recommended.",
    rating=5,
    place=place,
    user=user
)
```

### Adding Amenities

```python
from app.models.amenity import Amenity

wifi = Amenity(name="Wi-Fi")
parking = Amenity(name="Parking")

place.add_amenity(wifi)
place.add_amenity(parking)
```

## Why UUIDs?

This application uses UUIDs (Universally Unique Identifiers) instead of sequential numeric IDs for several reasons:

1. **Global Uniqueness**: UUIDs are unique across different systems and databases
2. **Security**: Non-sequential IDs prevent guessing valid identifiers
3. **Scalability**: Support for distributed systems without ID conflicts
4. **Flexibility**: Easy data merging across multiple sources

## Notes

- All models include automatic timestamp management (created_at, updated_at)
- Validation is performed on all input data to ensure data integrity
- Relationships are bidirectional and automatically maintained
- The current implementation uses in-memory storage (will be replaced with database in Part 3)
```

## Instructions de déploiement

1. Créez le fichier `app/models/base_model.py` avec le code fourni
2. Créez les modèles dans `app/models/`:
   - `user.py`
   - `place.py`
   - `review.py`
   - `amenity.py`
3. Mettez à jour `app/models/__init__.py`
4. Créez le dossier `tests/` et ajoutez `test_models.py`
5. Exécutez les tests: `python tests/test_models.py`
6. Mettez à jour le README.md

Tous les modèles sont maintenant implémentés avec:
- ✅ Validation complète des attributs
- ✅ Relations bidirectionnelles
- ✅ Gestion automatique des timestamps
- ✅ UUIDs comme identifiants
- ✅ Tests complets