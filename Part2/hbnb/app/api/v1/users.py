"""
User endpoints for the HBnB API.
Handles CRUD operations for users (Create, Read, Update).
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', max_length=50),
    'last_name': fields.String(required=True, description='Last name of the user', max_length=50),
    'email': fields.String(required=True, description='Email of the user')
})

# Define a separate model for updates (all fields optional)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user', max_length=50),
    'last_name': fields.String(required=False, description='Last name of the user', max_length=50),
    'email': fields.String(required=False, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check for email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'created_at': new_user.created_at.isoformat(),
                'updated_at': new_user.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        try:
            users = facade.get_all_users()
            return [
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'created_at': user.created_at.isoformat(),
                    'updated_at': user.updated_at.isoformat()
                }
                for user in users
            ], 200
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat()
            }, 200
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already registered')
    def put(self, user_id):
        """Update user information"""
        user_data = api.payload

        # Validate that at least one field is provided
        if not user_data:
            return {'error': 'No data provided for update'}, 400

        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Check if email is being changed and if it's already taken by another user
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
                
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'created_at': updated_user.created_at.isoformat(),
                'updated_at': updated_user.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'An error occurred while updating the user: {str(e)}'}, 500