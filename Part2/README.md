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