```mermaid
sequenceDiagram
    participant User
    participant API as Presentation Layer (API)
    participant Facade as Facade Pattern
    participant BL as Business Logic Layer (User  Model)
    participant DB as Persistence Layer (Database)


    User->>API: POST /api/users {first_name, last_name, email, password}
    API->>Facade: register_user(user_data)
    Facade->>BL: validate_user_data(user_data)
    BL-->>Facade: validation_result
    
    alt validation fails
        Facade-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        Facade->>BL: create_user(user_data)
        BL->>BL: hash_password()
        BL->>BL: generate_uuid()
        BL->>BL: set_timestamps()
        BL->>DB: save_user(user_object)
        DB-->>BL: user_saved_confirmation
        BL-->>Facade: user_created
        Facade-->>API: user_response
        API-->>User: 201 Created {id, first_name, last_name, email}
    end
