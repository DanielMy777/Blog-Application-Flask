# Blog Application (Flask)

This modest blog application acts as a web server developed under the Flask web framework.
The application was written entirely in python and included several libraries (see requirements file)

## ⚡️ Quick Start

> To start the app using docker-compose

1. Clone the repository (Or download the files).
2. In the terminnal, reach the root directory of this project. 
3. run `docker-compose up`..

> To start the app with python

1. Clone the repository (Or download the files).
2. In the terminnal, run `python <path to app.py>`.
3. To run the tests, run `pytest src/tests/` (after pytest has been installed).

## 👨‍💻 Technical Features
* Automatic swagger documentation. (exposed on the root / endpoint)
* Caching.
* Authentication & Security
* Containerization (Currently pulling the image from docker hub but you can use the dockerfile as well)
* Tests

## 😁 Behavioural Features
* Creating a new user and logging in as an existing user.
* Creating, getting, deleting and editing blog posts.
* Commenting and liking blog posts.

## ⚙️ Configurations To Docker-Compose
* In case port 5000 is already in use on your machine: 
    1. Change the app ports to `<new_port>:5000`.
* In case port 5432 is already in use on your machine:
    1. Change the postgres ports to `<new_port>:5432`.
    2. Change env var `POSTGRES_SERVICE` to `postgres:<new_port>`.
    3. Change env var `PGPORT` to `<new_port>`.
* In case port 6379 is already in use on your machine:
    1. Change the redis ports to `<new_port>:6379`.
    2. Change env var `CACHE_REDIS_PORT` to `<new_port>`.
    3. Change env var `CACHE_REDIS_URL` to `redis://redis:<new_port>/0`.

## 📖 Manual!
* To register, you must enter a username & password (non empty). You cannot use a username thats already taken.
* To login, you must enter a valid (registered) username & password.
* To use any of the blogpost endpoints, you need to add an 'Authorization' header to your requests. Get onr from the 'token' field of the login response and use the 'Authorization' header with the value `Bearer <token>`.
* To add a new post, you must include a valid title & content.
* To edit a new post, you may include a valid title & content.
* A valid title is a non empty string, of at most 20 characters.
* A valid post content is a non empty string, of at most 1000 characters.
* To comment on a post, you must include a valid content. A valid comment content is a non empty string, with at most 1000 characters AND does not include a curse word (for now, only the word 'curse' is a curse word).
* To delete or edit a post, you must be logged in as the post creator.
* To like a post, use the `blogpost/{post_id}/like` endpoint. To remove your like, use it again!


## ⭐️ Contributors

* Daniel Malky

> Feel free to add any contribution, it will be blessed.
