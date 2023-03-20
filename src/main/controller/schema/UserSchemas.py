from flask_restx import fields, reqparse
from src.main.model.model_utils.ModelUtils import validated_input

# === Helpful schemas to use as input & output in the user namespace

user_schema = {
    'username': fields.String(required=True, readonly=True, description='The username'),
    'password': fields.String(required=True, readonly=True, description='The pass'),
    'user_id': fields.Integer(required=True, readonly=True, description='The amount of likes'),
}

success_schema = {
    'status': fields.String(required=True, description='The status of the request')
}

login_schema = {
    'status': fields.String(required=True, description='The status of the request'),
    'token': fields.String(required=True, description='The JWT token provided')
}

parser = reqparse.RequestParser()
parser.add_argument('username', type=validated_input('Username', ['non_empty'], {}),
                    required=True, trim=True, help='Username is required.', location='json')
parser.add_argument('password', type=validated_input('Password', ['non_empty'], {}),
                    required=True, trim=True, help='Password is required.', location='json')
