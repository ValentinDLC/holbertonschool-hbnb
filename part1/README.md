
# HBnB - UML

Littre intro there

 This project organises an application into three main layers:
- Presentation Layer
Manages the user interface and APIs.
Serves as the entry point for all user requests.

- Business Logic Layer

Contains the business logic and main entities: User, Place, Review, Amenity.
Applies business rules and prepares data for persistence.

- Persistence Layer
Manages data storage via the database (DatabaseAccess) or files (FilesStorage) and this is the responsible for reading and writing data.

## 1 -  High-Level Architecture: 

### How it works

Requests start in the presentation layer, pass through the business layer façade, which applies the rules, and descend to the persistence layer to store or retrieve data.

The results are then sent back up to the presentation layer to be displayed to the user.

The class diagram illustrates the relationships between the layers and the main entities.

### Patterns used

Facade Pattern: simplifies access from the presentation layer to the business logic.

### Aggregation/lightweight linkage between layers:
 The presentation uses business logic, the business logic uses persistence.

## 2 - Business Logic Layer: 
This Layer contains the class diagram that represents the internal structure of the Business Logic Layer. 
It models the entities and their relationships.

### Entities
- User : Represents a person registered on the platform.
- Place : Represents a property available for rent.
- Review : Represents a comment left by a user about a property.
- Amenity : Represents the amenities of a property (WiFi, swimming pool, parking, etc...).
- BaseModel : Parent model that all others inherit from. It contains common attributes(`id`, `create_date`, `update_date`) and methods(`create`, `update`, `delete`).

### Relationships

- User -> Place (One-To-Many):
A user can own multiples properties
- User -> Review (One-To-Many)
A user can write several reviews
- Place -> Review (One-To-Many):
A place can have multiple reviews
- Place <-> Amenity (Many-To-Many):
A place can have multiples amenities and an amenity can have multiples places

## 3 - API Interaction Flow: 
Include the sequence diagrams for the selected API calls, providing explanations of the interactions and data flow between components.


# System Diagrams Documentation

---

## Diagram 1: User Registration

### Purpose
This diagram shows how a new user is registered in the system.

---

### Flow Breakdown

#### **Step 1: User Initiates Registration**
- **User → API**: `POST /api/users {first_name, last_name, email, password}`
- **Action**: User sends a POST request with registration data.
- **Data**: First name, last name, email, and password.

#### **Step 2: API Delegates to Facade**
- **API → Facade**: `register_user(user_data)`
- **Reason**: API doesn’t handle business logic directly.
- **Facade role**: Orchestrate the registration process.

#### **Step 3: Validation**
- **Facade → Business Logic**: `validate_user_data(user_data)`
- **Business Logic → Facade**: `validation_result`
- **Checks performed**:
  - Email format is valid
  - Password meets strength requirements
  - Required fields are present
  - Email is not already in use

#### **Step 4: Decision Point (alt block)**
- **If Validation Fails**:
  - **Facade → API**: `ValidationError`
  - **API → User**: `400 Bad Request`
  - **Result**: Returns immediately, no DB operation occurs.
- **If Validation Succeeds**:
  - **Facade → Business Logic**: `create_user(user_data)`

#### **Step 5: User Object Creation**
Business Logic performs:
1. `hash_password()` – **Security**: Never store plain passwords  
2. `generate_uuid()` – **Unique identifier**  
3. `set_timestamps()` – `created_at`, `updated_at`

#### **Step 6: Persist to Database**
- **Business Logic → Database**: `save_user(user_object)`
- **Database → Business Logic**: `user_saved_confirmation`

#### **Step 7: Success Response**
- **Business Logic → Facade**: `user_created`
- **Facade → API**: `user_response`
- **API → User**:  
  `201 Created {id, first_name, last_name, email}`  
  ⚠️ Password is **not returned**.

---

### Key Takeaways
- **Separation of Concerns**: Each layer has a specific role.  
- **Security**: Password hashing in Business Logic.  
- **Validation First**: Prevent expensive operations on invalid data.  
- **UUID Generation**: Ensures unique IDs across distributed systems.  

---

## Diagram 2: Fetching Places with Filters

### Purpose
Retrieve a list of places based on user-specified criteria (location, price range, etc.).

---

### Flow Breakdown

#### **Step 1: User Requests Places**
- **User → API**: `GET /api/places?filters={criteria}`
- **Example filters**:
  - `location=Paris`
  - `min_price=50&max_price=200`
  - `amenities=wifi,parking`

#### **Step 2: Facade Orchestration**
- **API → Facade**: `get_places(filters)`
- **Facade → Business Logic**: `validate_filters(filters)`
- **Checks**:
  - Price range valid (`min < max`)
  - Location format correct
  - Supported filter types

#### **Step 3: Query Database**
- **Business Logic → Database**: `fetch_places_with_filters(filters)`
- **Database → Business Logic**: `raw_places_list`

#### **Step 4: Data Enrichment (loop)**
For each place:
1. **Fetch amenities**  
   `Business Logic → Database: fetch_amenities(place_id)`  
   `Database → Business Logic: amenities_for_place`
2. **Fetch owner details**  
   `Business Logic → Database: fetch_owner(owner_id)`  
   `Database → Business Logic: owner_details`
3. **Combine data**  
   `Business Logic: enrich_place_data(place, amenities, owner)`


#### **Step 5: Return Enriched Data**
- **Business Logic → Facade**: `enriched_places_list`
- **Facade → API**: `places_response`
- **API → User**:  
  `200 OK [{id, title, description, price, latitude, longitude, amenities[], owner_info}]`

---

### Key Takeaways
- **Data Enrichment**: Combine related info (amenities, owners).  
- **Performance Consideration**: Optimize multiple DB queries.  
- **Complex Response**: Nested structures required.  
- **Filter Validation**: Prevents invalid queries.  

---

## Diagram 3: Creating a Place

### Purpose
Allow a property owner to create a new place listing.

---

### Flow Breakdown

#### **Step 1: User Submits Place Data**
- **User → API**:  
  `POST /api/places {title, description, price, latitude, longitude, owner_id, amenity_ids[]}`

#### **Step 2: Owner Verification**
- **Facade → Business Logic**: `verify_user_exists(owner_id)`
- **Business Logic → Database**: `get_user(owner_id)`
- **Critical**: Prevent orphaned records by ensuring owner exists.

#### **Step 3: Data Validation**
- **Checks**:
  - Title not empty
  - Price positive
  - Latitude/Longitude valid
  - Description length valid

#### **Step 4: Decision Point**
- **If invalid** → `400/401 Error`
- **If valid** → Proceed to creation

#### **Step 5: Create Place Object**
- **Business Logic**:
  - `generate_uuid()`
  - `set_timestamps()`
- **Business Logic → Database**: `save_place(place_object)`

#### **Step 6: Link Amenities (loop)**
For each amenity:
- **Business Logic → Database**: `link_amenity_to_place(place_id, amenity_id)`

#### **Step 7: Success Response**
- **API → User**:  
  `201 Created {id, title, description, price, latitude, longitude, amenity_ids[]}`

---

### Key Takeaways
- **Referential Integrity**: Ensure related entities exist.  
- **Many-to-Many**: Handled via junction table.  
- **Atomic Operations**: All links succeed or rollback.  
- **201 Created**: Correct HTTP response.  

---

## Diagram 4: Submitting a Review

### Purpose
Allow users to review places they’ve visited.

---

### Flow Breakdown

#### **Step 1: User Submits Review**
- **User → API**:  
  `POST /api/reviews {place_id, user_id, rating, comment}`

#### **Step 2: Place Verification**
- **Facade → Business Logic**: `check_place_exists(place_id)`

#### **Step 3: User Verification**
- **Facade → Business Logic**: `check_user_exists(user_id)`
- Ensures user exists before submitting review.

#### **Step 4: Review Validation**
- **Checks**:
  - Rating within allowed range
  - Comment not empty/too long
  - User hasn’t already reviewed

#### **Step 5: Decision Point**
- **If invalid** → `400/404 Error`
- **If valid** → Continue

#### **Step 6: Create and Save Review**
- **Business Logic**:
  - `generate_uuid()`
  - `set_timestamps()`
- **Business Logic → Database**: `save_review(review_object)`

#### **Step 7: Success Response**
- **API → User**:  
  `201 Created {id, place_id, user_id, rating, comment, timestamps}`

---

### Key Takeaways
- **Multiple Entity Verification**: Place + User must exist.  
- **Business Rules**: Rating limits, duplicate prevention.  
- **Audit Trail**: Timestamps ensure accountability.  
- **Error Specificity**: Different errors for different failures.  

---

