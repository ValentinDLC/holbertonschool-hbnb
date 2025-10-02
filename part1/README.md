
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

