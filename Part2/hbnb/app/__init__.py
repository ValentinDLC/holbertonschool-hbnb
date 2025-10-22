from flask import Flask
from flask_restx import Api
import os
from config import config  # Added: Import config

def create_app():
    app = Flask(__name__)
    # Added: Load configuration based on FLASK_ENV (defaults to 'development')
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config.get(env, config['default']))
    
    api = Api(app, version='1.0', title='Hbnb API', description='Hbnb Application API', doc='/api/v1/')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app