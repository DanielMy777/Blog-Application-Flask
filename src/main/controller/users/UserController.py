from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required
from src.main.service.users.UserService import UserService
from src.main.controller.schema.UserSchemas import user_schema, success_schema, login_schema, parser

# === Creating a new namespace, and configuring input & output schemas

user_ns = Namespace('user', description='User operations')

response_schema = user_ns.model('User', user_schema)

success_response_schema = user_ns.model('Success', success_schema)

success_login_schema = user_ns.model('Login', login_schema)


# ====== Controller classes, responsible of routing in the user namespace


@user_ns.route('/')
class UserController(Resource):
    @user_ns.marshal_list_with(response_schema)
    @jwt_required()
    @user_ns.doc(description='Get all the users')
    # === GET / to get all users
    def get(self):
        results = UserService.get_all_users()
        return [u.serialize for u in results], 200

    @ user_ns.marshal_with(success_response_schema, code=201)
    @user_ns.expect(parser)
    @user_ns.response(400, 'Validation error')
    @user_ns.doc(description='Register a new user')
    # === Post / to add a new user
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        UserService.create_user(username, password)
        return {'status': f'successfully created user "{username}"'}, 201


@user_ns.route('/login')
class UserLoginController(Resource):
    @ user_ns.marshal_with(success_login_schema)
    @user_ns.expect(parser)
    @user_ns.response(400, 'Bad Credentials')
    @user_ns.doc(description='Login to an existing user')
    # === POST / to login as a user
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        token = UserService.auth_user(username, password)
        return {'status': 'successful login', 'token': token}, 200
