```mermaid
sequenceDiagram
    participant User
    participant API as Presentation Layer (API)
    participant Facade as Facade Pattern
    participant BL as Business Logic Layer (User  & Place Models)
    participant DB as Persistence Layer (Database)


    User->>API: POST /api/places {title, description, price, latitude, longitude, owner_id, amenity_ids[]}
    API->>Facade: create_place(place_data, owner_id)
    Facade->>BL: verify_user_exists(owner_id)
    BL->>DB: get_user(owner_id)
    DB-->>BL: user_data
    BL-->>Facade: user_verified
    
    Facade->>BL: validate_place_data(place_data)
    BL-->>Facade: validation_result
    
    alt validation fails or user not found
        Facade-->>API: ValidationError or NotFoundError
        API-->>User: 400/404 Error
    else validation succeeds
        Facade->>BL: create_place_object(place_data, owner_id)
        BL->>BL: generate_uuid()
        BL->>BL: set_timestamps()
        BL->>DB: save_place(place_object)
        DB-->>BL: place_saved
        
        loop for each amenity_id in amenity_ids[]
            BL->>DB: link_amenity_to_place(place_id, amenity_id)
            DB-->>BL: link_confirmed
        end
        
        BL-->>Facade: place_created
        Facade-->>API: place_response
        API-->>User: 201 Created {id, title, description, price, latitude, longitude, amenity_ids[]}
    end
