```mermaid
sequenceDiagram
    participant User
    participant API as Presentation Layer (API)
    participant Facade as Facade Pattern
    participant BL as Business Logic Layer (Place, Amenity & User Models)
    participant DB as Persistence Layer (Database)


    User->>API: GET /api/places?filters={criteria e.g., location, price}
    API->>Facade: get_places(filters)
    Facade->>BL: validate_filters(filters)
    BL-->>Facade: validation_result
    
    alt validation fails
        Facade-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        Facade->>BL: query_places(filters)
        BL->>DB: fetch_places_with_filters(filters)
        DB-->>BL: raw_places_list
        
        loop for each place in places_list
            BL->>DB: fetch_amenities(place_id)
            DB-->>BL: amenities_for_place
            BL->>DB: fetch_owner(owner_id)
            DB-->>BL: owner_details
            BL->>BL: enrich_place_data(place, amenities, owner)
        end
        
        BL-->>Facade: enriched_places_list
        Facade-->>API: places_response
        API-->>User: 200 OK [{id, title, description, price, latitude, longitude, amenities[], owner_info}]
    end
