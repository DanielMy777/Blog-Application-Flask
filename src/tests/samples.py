from src.main.model.User import User
from src.main.model.Post import Post
from src.main.model.Comment import Comment
from werkzeug.security import generate_password_hash

# ====== Model samples used for testing

s_user_1 = User('test-user-1', generate_password_hash('test-pass-1'))
s_user_2 = User('test-user-2', generate_password_hash('test-pass-2'))

s_post_1 = Post('Test Post 1', 'Content for test post 1', 1)
s_post_2 = Post('Test Post 2', 'Content for test post 2', 2)

s_comment_1 = Comment('Test Comment 1', 1, 1)
s_comment_2 = Comment('Test Comment 2', 2, 1)
