from src.main.model.model_utils.ModelUtils import db
from src.main.model.Post import Post
from src.main.model.User import User
from src.main.model.PostLikes import PostLikes  # needed
from src.main.model.Comment import Comment  # needed


# ====== DAO class, responsible for querying the DB in the blogpost namespace

class PostDAO():
    def get_all_posts():
        return Post.query.all()

    def get_post(id):
        return Post.query.get(id)

    def create_post(post):
        db.session.add(post)
        db.session.commit()

    def delete_post(post_id):
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()

    def edit_post(post_id, title=None, content=None):
        post = Post.query.get(post_id)
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        db.session.commit()

    def add_comment(comment):
        db.session.add(comment)
        db.session.commit()

    def add_like(post_id, liker_id):
        post = Post.query.get(post_id)
        user = User.query.get(liker_id)
        post.likes.append(user)
        db.session.commit()

    def remove_like(post_id, user_id):
        post = Post.query.get(post_id)
        user = User.query.get(user_id)
        post.likes.remove(user)
        db.session.commit()
