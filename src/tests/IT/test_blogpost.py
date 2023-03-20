from src.tests.conftests import app_db, app, db, client, token_1, token_2
from src.main.model.User import User
from src.main.model.Post import Post

# =============== IT tests in the blogpost namespace


def test_no_auth_should_fail(client):
    response = client.get('/blogpost/')
    assert response.status_code == 401


def test_bad_auth_should_fail(client, token_1):
    response = client.get('/blogpost/',
                          headers={'Authorization': f'Bearer {token_1[:-1]}'})
    assert response.status_code == 422


def test_get_all_posts_should_succeed(client, token_1, app):
    response = client.get('/blogpost/',
                          headers={'Authorization': f'Bearer {token_1}'})
    posts = response.json
    assert response.status_code == 200
    assert len(posts) == 2, "Number of initial posts in the db should be 2"
    with app.app_context():
        assert posts[0]['title'] == Post.query.first().title


def test_get_post_should_succeed(client, token_1, app):
    post_id = 1
    response = client.get(f'/blogpost/{post_id}',
                          headers={'Authorization': f'Bearer {token_1}'})
    post = response.json
    assert response.status_code == 200
    with app.app_context():
        assert post['title'] == Post.query.get(post_id).title


def test_get_non_existing_post_should_fail(client, token_1, app):
    post_id = 5
    response = client.get(f'/blogpost/{post_id}',
                          headers={'Authorization': f'Bearer {token_1}'})
    assert response.status_code == 400


def test_add_post_should_succeed(client, token_1, app):
    new_post = {'title': 'New Post', 'content': 'New Content'}
    response = client.post('/blogpost/',
                           headers={'Authorization': f'Bearer {token_1}'},
                           json=new_post)
    assert response.status_code == 201
    with app.app_context():
        assert Post.query.count() == 3, "Adding a new post should make the count 3"


def test_add_post_empty_field_should_fail(client, token_1, app):
    new_post = {'title': 'New Post', 'content': ''}
    response = client.post('/blogpost/',
                           headers={'Authorization': f'Bearer {token_1}'},
                           json=new_post)
    msg = response.json
    assert response.status_code == 400
    assert 'empty' in msg['errors']['content']


def test_add_post_limited_field_should_fail(client, token_1, app):
    new_post = {'title': 'a'*21, 'content': 'New Content'}
    response = client.post('/blogpost/',
                           headers={'Authorization': f'Bearer {token_1}'},
                           json=new_post)
    msg = response.json
    assert response.status_code == 400
    assert 'maximum' in msg['errors']['title']


def test_add_comment_should_succeed(client, token_1, app):
    post_id = 1
    new_content = 'New Comment'
    with app.app_context():
        before_comments = len(Post.query.get(post_id).comments)
    new_comment = {'content': new_content}
    response = client.post(f'/blogpost/{post_id}/comment',
                           headers={'Authorization': f'Bearer {token_1}'},
                           json=new_comment)
    with app.app_context():
        after_comments = len(Post.query.get(post_id).comments)
        new_com = Post.query.get(post_id).comments[-1]
    assert response.status_code == 201
    assert after_comments == before_comments + 1
    assert new_com.content == new_content


def test_add_comment_non_existing_post_should_fail(client, token_1, app):
    post_id = 5
    new_content = 'New Comment'
    new_comment = {'content': new_content}
    response = client.post(f'/blogpost/{post_id}/comment',
                           headers={'Authorization': f'Bearer {token_1}'},
                           json=new_comment)
    assert response.status_code == 400


def test_add_comment_curse_should_fail(client, token_1, app):
    post_id = 1
    new_content = 'New curse comment'
    new_comment = {'content': new_content}
    response = client.post(f'/blogpost/{post_id}/comment',
                           headers={'Authorization': f'Bearer {token_1}'},
                           json=new_comment)
    assert response.status_code == 400
    assert 'curse' in response.json['errors']['content']


def test_add_like_should_succeed(client, token_1, app):
    post_id = 1
    with app.app_context():
        before_likes = Post.query.get(post_id).likes
    response = client.post(f'/blogpost/{post_id}/like',
                           headers={'Authorization': f'Bearer {token_1}'})
    with app.app_context():
        after_likes = Post.query.get(post_id).likes
    assert response.status_code == 200
    with app.app_context():
        assert len(after_likes) == len(before_likes) + 1
        assert after_likes[-1].username == User.query.get(post_id).username


def test_remove_like_should_succeed(client, token_2, app):
    post_id = 1
    with app.app_context():
        before_likes = Post.query.get(post_id).likes
    response_1 = client.post(f'/blogpost/{post_id}/like',
                             headers={'Authorization': f'Bearer {token_2}'})
    response_2 = client.post(f'/blogpost/{post_id}/like',
                             headers={'Authorization': f'Bearer {token_2}'})
    with app.app_context():
        after_likes = Post.query.get(post_id).likes
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    with app.app_context():
        assert len(after_likes) == len(before_likes)


def test_edit_post_should_succeed(client, token_1, app):
    post_id = 1
    new_content = 'New Content'
    params = {'content': new_content}
    response = client.patch(f'/blogpost/{post_id}',
                            headers={'Authorization': f'Bearer {token_1}'},
                            json=params)
    assert response.status_code == 200
    with app.app_context():
        assert Post.query.get(post_id).content == new_content


def test_edit_post_empty_field_should_fail(client, token_1, app):
    post_id = 1
    params = {'title': 'New Post', 'content': ''}
    response = client.patch(f'/blogpost/{post_id}',
                            headers={'Authorization': f'Bearer {token_1}'},
                            json=params)
    msg = response.json
    assert response.status_code == 400
    assert 'empty' in msg['errors']['content']


def test_edit_post_limited_field_should_fail(client, token_1, app):
    post_id = 1
    params = {'title': 'a'*21, 'content': 'New Content'}
    response = client.patch(f'/blogpost/{post_id}',
                            headers={'Authorization': f'Bearer {token_1}'},
                            json=params)
    msg = response.json
    assert response.status_code == 400
    assert 'maximum' in msg['errors']['title']


def test_edit_someone_else_post_should_fail(client, token_2, app):
    post_id = 1
    params = {'title': 'New Title', 'content': 'New Content'}
    response = client.patch(f'/blogpost/{post_id}',
                            headers={'Authorization': f'Bearer {token_2}'},
                            json=params)
    assert response.status_code == 403


def test_delete_post_should_succeed(client, token_1, app):
    post_id = 1
    response = client.delete(f'/blogpost/{post_id}',
                             headers={'Authorization': f'Bearer {token_1}'})
    assert response.status_code == 204
    with app.app_context():
        assert Post.query.get(post_id) is None


def test_delete_someone_elses_post_should_fail(client, token_1, app):
    post_id = 2
    response = client.delete(f'/blogpost/{post_id}',
                             headers={'Authorization': f'Bearer {token_1}'})
    assert response.status_code == 403
    with app.app_context():
        assert Post.query.get(post_id) is not None
