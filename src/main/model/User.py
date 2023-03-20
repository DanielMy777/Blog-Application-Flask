from src.main.model.model_utils.ModelUtils import db

# === User Model


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')
    liked = db.relationship('Post', secondary='post_likes',
                            back_populates='likes')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def serialize(self):
        return {"username": self.username,
                "password": self.password,
                "user_id": self.id}
