from flask_restx import Resource, Namespace
from src.main.service.posts.PostService import PostService
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.main.controller.schema.PostSchemas import success_schema, comment_schema, post_schema
from src.main.controller.schema.PostSchemas import post_parser, comment_parser
from src.main.model.model_utils.ModelUtils import cache

# === Creating a new namespace, and configuring input & output schemas
blogpost_ns = Namespace('blogpost', description='Blog post operations')

post_response_schema = blogpost_ns.model('Post', post_schema)

comment_response_schema = blogpost_ns.model('Comment', comment_schema)


success_response_schema = blogpost_ns.model('Success', success_schema)

no_content_schema = blogpost_ns.model('NC', {})


# ====== Controller classes, responsible of routing in the blogpost namespace


@ blogpost_ns.route('/')
class PostController(Resource):
    @ blogpost_ns.marshal_list_with(post_response_schema)
    @ jwt_required()
    @ cache.cached(timeout=10)
    @blogpost_ns.doc(description='Get all the posts')
    # === GET / to get all posts
    def get(self):
        results = PostService.get_all_posts()
        ser_res = [p.serialize for p in results]
        return ser_res, 200

    @ blogpost_ns.marshal_with(success_response_schema, code=201)
    @blogpost_ns.expect(post_parser(True))
    @blogpost_ns.response(400, 'Validation error')
    @ jwt_required()
    @blogpost_ns.doc(description='Post a new blog post')
    # === POST / to add a post
    def post(self):
        args = post_parser(True).parse_args()
        title = args['title']
        content = args['content']
        author = get_jwt_identity()
        PostService.create_post(
            title, content, author)
        clear_cache(None)
        return {'status': f'successfully created post "{title}"'}, 201


@ blogpost_ns.route('/<int:post_id>', doc={'params': {'post_id': 'The post ID to get'}})
class PostWithIDController(Resource):
    @ blogpost_ns.marshal_with(post_response_schema)
    @blogpost_ns.response(400, 'ID not exist')
    @ jwt_required()
    @ cache.cached(timeout=30)
    @blogpost_ns.doc(description='Get a specific post')
    # === GET /{post_id} to get a post
    def get(self, post_id):
        return PostService.get_post(post_id).serialize, 200

    @ blogpost_ns.marshal_with(no_content_schema, code=204)
    @blogpost_ns.response(400, 'ID not exist')
    @blogpost_ns.response(403, 'Forbidden for the user')
    @ jwt_required()
    @blogpost_ns.doc(description='Delete a specific post')
    # === DELETE /{post_id} to delete a post
    def delete(self, post_id):
        author = get_jwt_identity()
        PostService.delete_post(post_id, author)
        clear_cache(post_id)
        return {}, 204

    @ blogpost_ns.marshal_with(post_response_schema)
    @blogpost_ns.response(400, 'ID not exist')
    @blogpost_ns.response(403, 'Forbidden for the user')
    @blogpost_ns.expect(post_parser(False))
    @ jwt_required()
    @blogpost_ns.doc(description='Edit a specific post')
    # === PATCH /{post_id} to edit a post
    def patch(self, post_id):
        args = post_parser(False).parse_args()
        title = args['title']
        content = args['content']
        author = get_jwt_identity()
        PostService.edit_post(
            post_id, title, content, author)
        clear_cache(post_id)
        return PostService.get_post(post_id).serialize, 200


@ blogpost_ns.route('/<int:post_id>/comment', doc={'params': {'post_id': 'The post ID to get'}})
class PostCommentController(Resource):
    @ blogpost_ns.marshal_with(post_response_schema, code=201)
    @blogpost_ns.response(400, 'ID not exist | Validation Error')
    @blogpost_ns.expect(comment_parser)
    @ jwt_required()
    @blogpost_ns.doc(description='Comment on a specific post')
    # === POST /{post_id}/comment to comment on a post
    def post(self, post_id):
        args = comment_parser.parse_args()
        content = args['content']
        author = get_jwt_identity()
        PostService.create_comment(
            content, post_id, author)
        clear_cache(post_id)
        return PostService.get_post(post_id).serialize, 201


@ blogpost_ns.route('/<int:post_id>/like', doc={'params': {'post_id': 'The post ID to get'}})
class PostLikeController(Resource):
    @ blogpost_ns.marshal_with(post_response_schema)
    @blogpost_ns.response(400, 'ID not exist')
    @ jwt_required()
    @blogpost_ns.doc(description='Like or unlike a specfic post')
    # === POST /{post_id}/like to like or unlike a post
    def post(self, post_id):
        user_id = get_jwt_identity()
        PostService.trigger_like(post_id, user_id)
        clear_cache(post_id)
        return PostService.get_post(post_id).serialize, 200


# === Help method to clear cache items that are connected to a changed post
def clear_cache(post_id):
    path_all = f"view//{blogpost_ns.name}/"
    cache.delete(path_all)
    if post_id is not None:
        path_post = path_all + str(post_id)
        cache.delete(path_post)
