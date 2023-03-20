from flask import abort
from src.main.dao.posts.PostDAO import PostDAO
from src.main.model.Post import Post
from src.main.model.Comment import Comment

# === Service class, responsible of handling the business login in the blogpost namespace


class PostService():
    def get_all_posts():
        return PostDAO.get_all_posts()

    def get_post(post_id):
        post = PostDAO.get_post(post_id)
        if post:
            return post
        else:
            abort(400, f"No post found with id {post_id}.")

    def create_post(title, content, author_id):
        post = Post(title, content, author_id=author_id)
        PostDAO.create_post(post)

# todo code duplication in delete & edit
    def delete_post(post_id, user_id):
        post = PostDAO.get_post(post_id)
        if post:
            if post.author_id == user_id:
                PostDAO.delete_post(post_id)
            else:
                abort(
                    403, f"You must be the creator of this post in order to delete it!")
        else:
            abort(400, f"No post found with id {post_id}.")

    def edit_post(post_id, title, content, user_id):
        post = PostDAO.get_post(post_id)
        if post:
            if post.author_id == user_id:
                PostDAO.edit_post(post_id, title, content)
            else:
                abort(
                    403, f"You must be the creator of this post in order to edit it!")
        else:
            abort(400, f"No post found with id {post_id}.")

    def create_comment(content, post_id, author_id):
        post = PostDAO.get_post(post_id)
        if post:
            com = Comment(content, post_id=post_id, author_id=author_id)
            PostDAO.add_comment(com)
        else:
            abort(400, f"No post found with id {post_id}.")

    def trigger_like(post_id, liker_id):
        post = PostDAO.get_post(post_id)
        if post:
            if any([u.id == liker_id for u in post.likes]):
                PostDAO.remove_like(post_id, liker_id)
            else:
                PostDAO.add_like(post_id, liker_id)
        else:
            abort(400, f"No post found with id {post_id}.")
