"""
Place endpoints for the HBnB API.
Handles CRUD operations for places (Create, Read, Update).
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place', max_length=100),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenity IDs")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        try:
            # Create the place
            new_place = facade.create_place(place_data)
            
            # Handle amenities if provided
            if 'amenities' in place_data and place_data['amenities']:
                for amenity_id in place_data['amenities']:
                    try:
                        facade.add_amenity_to_place(new_place.id, amenity_id)
                    except ValueError:
                        # Skip invalid amenity IDs
                        pass
            
            # Include amenities in response for consistency with GET
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id,
                'amenities': [
                    {
                        'id': amenity.id,
                        'name': amenity.name
                    }
                    for amenity in (new_place.amenities or [])
                ],
                'created_at': new_place.created_at.isoformat(),
                'updated_at': new_place.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            return [
                {
                    'id': place.id,
                    'title': place.title,
                    'latitude': place.latitude,
                    'longitude': place.longitude,
                    'price': place.price
                }
                for place in places
            ], 200
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                },
                'amenities': [
                    {
                        'id': amenity.id,
                        'name': amenity.name
                    }
                    for amenity in (place.amenities or [])
                ],
                'reviews': [
                    {
                        'id': review.id,
                        'text': review.text,
                        'rating': review.rating,
                        'user_id': review.user.id
                    }
                    for review in (place.reviews or [])
                ],
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }, 200
        except AttributeError as e:
            return {'error': f'Missing attribute: {str(e)}'}, 500
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload

        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        try:
            # Update amenities if provided
            if 'amenities' in place_data:
                amenity_ids = place_data.pop('amenities')
                # Clear existing amenities
                place.amenities = []
                # Add new amenities
                for amenity_id in amenity_ids:
                    try:
                        facade.add_amenity_to_place(place_id, amenity_id)
                    except ValueError:
                        pass
            
            # Update place data
            updated_place = facade.update_place(place_id, place_data)
            
            # Include amenities in response for consistency with GET
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner.id,
                'amenities': [
                    {
                        'id': amenity.id,
                        'name': amenity.name
                    }
                    for amenity in (updated_place.amenities or [])
                ],
                'created_at': updated_place.created_at.isoformat(),
                'updated_at': updated_place.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'An error occurred while updating: {str(e)}'}, 500


@api.route('/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Get all reviews for this place
            reviews = facade.get_reviews_by_place(place_id)
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id,
                    'created_at': review.created_at.isoformat(),
                    'updated_at': review.updated_at.isoformat()
                }
                for review in reviews
            ], 200
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500