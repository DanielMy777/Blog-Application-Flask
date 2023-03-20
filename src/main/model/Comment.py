from src.main.model.model_utils.ModelUtils import db

# === Comment Model


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, content, author_id, post_id):
        self.content = content
        self.author_id = author_id
        self.post_id = post_id

    def __repr__(self):
        return f"<Comment {self.content[:20]}{'...' if self.content.length >= 20 else ''}>"

    @property
    def serialize(self):
        return {"content": self.content,
                "commented": self.user.username}
