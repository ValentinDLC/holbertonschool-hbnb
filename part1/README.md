
# HBnB - UML

Littre intro there

## 1 -  High-Level Architecture: 
- This project organises an application into three main layers:
- Presentation Layer
Manages the user interface and APIs.
Serves as the entry point for all user requests.

- Business Logic Layer

Contains the business logic and main entities: User, Place, Review, Amenity.
Applies business rules and prepares data for persistence.

- Persistence Layer
Manages data storage via the database (DatabaseAccess) or files (FilesStorage).
Responsible for reading and writing data.

- How it works
Requests start in the presentation layer, pass through the business layer façade, which applies the rules, and descend to the persistence layer to store or retrieve data.

The results are then sent back up to the presentation layer to be displayed to the user.

The class diagram illustrates the relationships between the layers and the main entities.

- Patterns used

Facade Pattern: simplifies access from the presentation layer to the business logic.

- Aggregation/lightweight linkage between layers: the presentation uses business logic, the business logic uses persistence.

## 2 - Business Logic Layer: 
Present the detailed class diagram, explaining the entities, their relationships, and how they fit into the business logic of the application.

## 3 - API Interaction Flow: 
Include the sequence diagrams for the selected API calls, providing explanations of the interactions and data flow between components.

