from src.main.model.model_utils.ModelUtils import db

# === Post Model


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post')
    likes = db.relationship('User', secondary='post_likes',
                            back_populates='liked')

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id

    def __repr__(self):
        return f"<Post {self.title}>"

    @property
    def serialize(self):
        return {"title": self.title,
                "content": self.content,
                "likes": [l.username for l in self.likes],
                "author": self.user.username,
                "comments": [{"author": c.user.username, "content": c.content} for c in self.comments],
                "post_id": self.id
                }
