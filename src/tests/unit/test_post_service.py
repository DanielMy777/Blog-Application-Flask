import pytest
from pytest_mock import mocker
from src.main.service.posts.PostService import PostService
from src.main.dao.posts.PostDAO import PostDAO
from src.main.model.Post import Post
from src.main.model.User import User
import copy

sample_posts = [{'title': 'post1', 'content': 'abc'},
                {'title': 'post2', 'content': 'def'}]

# ====== Unit tests in the blogpost namespace


def test_get_all_posts_should_return(mocker):
    # arrange
    posts = sample_posts
    mocker.patch.object(PostDAO, 'get_all_posts', return_value=posts)
    # act
    result = PostService.get_all_posts()
    # assert
    assert len(result) == 2
    assert result[0]['title'] == 'post1'
    assert result[1]['title'] == 'post2'


def test_get_post_should_return(mocker):
    # arrange
    post = sample_posts[0]
    mocker.patch.object(PostDAO, 'get_post', return_value=post)
    # act
    result = PostService.get_post(1)
    # assert
    assert result['title'] == 'post1'


def test_get_non_exisiting_post_should_throw(mocker):
    # arrange
    mocker.patch.object(PostDAO, 'get_post', return_value=None)
    # act
    with pytest.raises(Exception) as e:
        PostService.get_post(1)
    # assert
    assert e._excinfo[0].code == 400


def test_create_post_should_pass(mocker):
    # arrange
    s_post = sample_posts[0]
    mocker.patch.object(PostDAO, 'create_post', return_value=None)
    # act
    result = PostService.create_post(s_post['title'], s_post['content'], 1)
    # assert
    assert result is None


def test_delete_post_should_pass(mocker):
    # arrange
    s_post = copy.deepcopy(sample_posts[0])
    post = Post(s_post['title'], s_post['content'], 1)
    mocker.patch.object(PostDAO, 'get_post', return_value=post)
    mocker.patch.object(PostDAO, 'delete_post', return_value=None)
    # act
    result = PostService.delete_post(1, 1)
    # assert
    assert result is None


def test_delete_non_exisiting_post_should_throw(mocker):
    # arrange
    mocker.patch.object(PostDAO, 'get_post', return_value=None)
    mocker.patch.object(PostDAO, 'delete_post', return_value=None)
    # act
    with pytest.raises(Exception) as e:
        PostService.delete_post(1, 1)
    # assert
    assert e._excinfo[0].code == 400


def test_delete_someone_elses_post_should_throw(mocker):
    # arrange
    s_post = copy.deepcopy(sample_posts[0])
    post = Post(s_post['title'], s_post['content'], 1)
    mocker.patch.object(PostDAO, 'get_post', return_value=post)
    mocker.patch.object(PostDAO, 'delete_post', return_value=None)
    # act
    with pytest.raises(Exception) as e:
        PostService.delete_post(1, 2)
    # assert
    assert e._excinfo[0].code == 403


def test_edit_post_should_pass(mocker):
    # arrange
    title = 'New Title'
    content = 'New Content'
    s_post = copy.deepcopy(sample_posts[0])
    post = Post(s_post['title'], s_post['content'], 1)
    mocker.patch.object(PostDAO, 'get_post', return_value=post)
    mocker.patch.object(PostDAO, 'edit_post', return_value=None)
    # act
    result = PostService.edit_post(1, title, content, 1)
    # assert
    assert result is None


def test_edit_non_exisiting_post_should_throw(mocker):
    # arrange
    title = 'New Title'
    content = 'New Content'
    mocker.patch.object(PostDAO, 'get_post', return_value=None)
    mocker.patch.object(PostDAO, 'edit_post', return_value=None)
    # act
    with pytest.raises(Exception) as e:
        PostService.edit_post(1, title, content, 1)
    # assert
    assert e._excinfo[0].code == 400


def test_edit_someone_elses_post_should_throw(mocker):
    # arrange
    title = 'New Title'
    content = 'New Content'
    s_post = copy.deepcopy(sample_posts[0])
    post = Post(s_post['title'], s_post['content'], 1)
    mocker.patch.object(PostDAO, 'get_post', return_value=post)
    mocker.patch.object(PostDAO, 'edit_post', return_value=None)
    # act
    with pytest.raises(Exception) as e:
        PostService.edit_post(1, title, content, 2)
    # assert
    assert e._excinfo[0].code == 403


def test_comment_should_pass(mocker):
    # arrange
    content = 'Comment'
    post = sample_posts[0]
    mocker.patch.object(PostDAO, 'get_post', return_value=post)
    mocker.patch.object(PostDAO, 'add_comment', return_value=None)
    # act
    result = PostService.create_comment(1, content, 1)
    # assert
    assert result is None


def test_comment_on_non_exisiting_post_should_throw(mocker):
    # arrange
    content = 'Comment'
    mocker.patch.object(PostDAO, 'get_post', return_value=None)
    mocker.patch.object(PostDAO, 'add_comment', return_value=None)
    # act
    with pytest.raises(Exception) as e:
        PostService.create_comment(1, content, 1)
    # assert
    assert e._excinfo[0].code == 400


def test_add_like_should_pass(mocker):
    # arrange
    s_post = sample_posts[0]
    post = Post(s_post['title'], s_post['content'], 1)
    mocker.patch.object(PostDAO, 'get_post', return_value=post)
    remove_mock = mocker.patch.object(
        PostDAO, 'remove_like', return_value=None)
    add_mock = mocker.patch.object(PostDAO, 'add_like', return_value=None)
    # act
    result = PostService.trigger_like(1, 1)
    # assert
    assert remove_mock.call_count == 0
    assert add_mock.call_count == 1
    assert result is None


def test_remove_like_should_pass(mocker):
    # arrange
    s_post = sample_posts[0]
    post = Post(s_post['title'], s_post['content'], 1)
    user = User('user', 'pass')
    post.likes.append(user)
    mocker.patch.object(PostDAO, 'get_post', return_value=post)
    remove_mock = mocker.patch.object(
        PostDAO, 'remove_like', return_value=None)
    add_mock = mocker.patch.object(PostDAO, 'add_like', return_value=None)
    # act
    result = PostService.trigger_like(1, user.id)
    # assert
    assert remove_mock.call_count == 1
    assert add_mock.call_count == 0
    assert result is None


def test_like_on_non_exisiting_post_should_throw(mocker):
    # arrange
    mocker.patch.object(PostDAO, 'get_post', return_value=None)
    mocker.patch.object(PostDAO, 'remove_like', return_value=None)
    mocker.patch.object(PostDAO, 'add_like', return_value=None)
    # act
    with pytest.raises(Exception) as e:
        PostService.trigger_like(1, 1)
    # assert
    assert e._excinfo[0].code == 400
