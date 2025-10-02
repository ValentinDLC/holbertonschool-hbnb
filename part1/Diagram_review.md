```mermaid
sequenceDiagram
    participant User
    participant API as Presentation Layer (API)
    participant Facade as Facade Pattern
    participant BL as Business Logic Layer (User , Place & Review Models)
    participant DB as Persistence Layer (Database)


    User->>API: POST /api/reviews {place_id, user_id, rating, comment}
    API->>Facade: submit_review(review_data)
    
    Facade->>BL: check_place_exists(place_id)
    BL->>DB: fetch_place(place_id)
    DB-->>BL: place_data or null
    BL-->>Facade: place_confirmed
    
    Facade->>BL: check_user_exists(user_id)
    BL->>DB: fetch_user(user_id)
    DB-->>BL: user_data or null
    BL-->>Facade: user_confirmed
    
    Facade->>BL: validate_review_data(review_data)
    BL-->>Facade: validation_result
    
    alt validation fails or place/user not found
        Facade-->>API: ValidationError or NotFoundError
        API-->>User: 400/404 Error
    else everything valid
        Facade->>BL: create_review_object(review_data)
        BL->>BL: generate_uuid()
        BL->>BL: set_timestamps()
        BL->>DB: save_review(review_object)
        DB-->>BL: review_saved
        BL-->>Facade: review_created
        Facade-->>API: review_response
        API-->>User: 201 Created {id, place_id, user_id, rating, comment, timestamps}
    end
