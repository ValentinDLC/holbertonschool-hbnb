``` mermaid
 ---
config:
  theme: dark
  look: neo
---
classDiagram
class PresentationLayer {
    API/Services
    User Interface
}
class BusinessLogicLayer {
    <<entity>> User 
    <<entity>> Place
    <<entity>> Review 
    <<entity>> Amenity
}
class PersistenceLayer {
    <<service>>DatabaseAccess
    <<service>>FilesStorage
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Storage Operation
