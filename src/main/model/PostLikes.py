from src.main.model.model_utils.ModelUtils import db

# === PostLikes Model (User_likes_Post relation)


class PostLikes(db.Model):
    __tablename__ = "post_likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
