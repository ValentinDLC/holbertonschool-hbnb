"""
Amenity endpoints for the HBnB API.
Handles CRUD operations for amenities (Create, Read, Update).
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity', max_length=50)
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Amenity already exists')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        
        # Validate name is not empty
        if not amenity_data.get('name') or not amenity_data.get('name').strip():
            return {'error': 'Amenity name is required and must be a string'}, 400
        
        try:
            # Check if amenity with same name already exists (case-insensitive)
            existing_amenities = facade.get_all_amenities()
            for amenity in existing_amenities:
                if amenity.name.lower().strip() == amenity_data['name'].lower().strip():
                    return {'error': 'Amenity with this name already exists'}, 409
            
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat(),
                'updated_at': amenity.updated_at.isoformat()
            }
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Amenity name already exists')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        
        # Check if amenity exists
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Validate name is not empty
        if not amenity_data.get('name') or not amenity_data.get('name').strip():
            return {'error': 'Amenity name is required and must be a string'}, 400
        
        try:
            # Check if another amenity with same name already exists (case-insensitive)
            existing_amenities = facade.get_all_amenities()
            for existing_amenity in existing_amenities:
                if (existing_amenity.id != amenity_id and 
                    existing_amenity.name.lower().strip() == amenity_data['name'].lower().strip()):
                    return {'error': 'Amenity with this name already exists'}, 409
            
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat(),
                'updated_at': updated_amenity.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Delete the amenity using facade
        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200