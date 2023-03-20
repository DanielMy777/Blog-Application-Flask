from flask_restx import fields, reqparse, Model
from src.main.model.model_utils.ModelUtils import validated_input

# === Helpful schemas to use as input & output in the blogpost namespace

comment_schema = {
    'author': fields.String(required=True, readonly=True, description='The username of the commenter'),
    'content': fields.String(required=True, readonly=True, description='The content of the comment'),

}

post_schema = {
    'title': fields.String(required=True, readonly=True, description='The title of the post'),
    'author': fields.String(required=True, readonly=True, description='The username of the poster'),
    'content': fields.String(required=True, readonly=True, description='The content of the post'),
    'likes': fields.List(cls_or_instance=fields.String, readonly=True, description='The usernames of likers'),
    'comments': fields.List(cls_or_instance=fields.Nested(Model('Comment', comment_schema)),
                            required=True, readonly=True, description='The comments on the post'),
    'post_id': fields.Integer(required=True, readonly=True, description='The post ID'),
}

success_schema = {
    'status': fields.String(required=True, description='The status of the request')
}


def post_parser(req):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title',
                             type=validated_input('Title', ['non_empty', 'limit'], {
                                 'max_length': 20}),
                             required=req, trim=True, help='Title is required.' if req else 'Bad Title.',
                             location='json')
    post_parser.add_argument('content',
                             type=validated_input('Content', ['non_empty', 'limit'], {
                                 'max_length': 1000}),
                             required=req, trim=True, help='Content is required.' if req else 'Bad Content.',
                             location='json')
    return post_parser


comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content',
                            type=validated_input('Content', ['non_empty', 'limit', 'clean'], {
                                'max_length': 1000}),
                            required=True, trim=True, help='Content is required.', location='json')
