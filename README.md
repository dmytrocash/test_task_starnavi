## TO DO

### Task 1. Social Network

Object of this task is to create a simple REST API. You can use one framework from this list (Django Rest Framework, Flask or FastAPI) and all libraries which you  prefer to use with these frameworks.

Basic models:
* User
* Post (always made by a user)

Basic Features:
* user signup
* user login
* post creation
* post like
* post unlike
* analytics about how many likes was made. API should return analytics aggregated by day. Example url:
/analytics?date_from=2020-02-02&date_to=2020-02-15
* user activity an endpoint which will show when user was login last time and when he made a last action to the service

Requirements:
* Implement token authentication (JWT is preferred)

### Task 2. Automated bot

Object of this bot demonstrate functionalities of the system according to defined rules. This bot
should read rules from a config file (in any format chosen by the candidate), but should have
following fields (all integers, candidate can rename as they see fit).
* number_of_users
* max_posts_per_user
* max_likes_per_user

Bot should read the configuration and create this activity:
* signup users (number provided in config)
* each user creates random number of posts with any content (up to
 max_posts_per_user)
* after creating the signup and posting activity, posts should be liked randomly, posts
 can be liked multiple times

Notes:
* clean and usable REST API is important
* bot is just separate python script, not a django management command or etc
* the project is not defined in detail, the candidate should use their best judgment for every non-specified requirements (including chosen tech, third party apps, etc), however every decision must be explained and backed by arguments in the interview
* result should be sent by providing a Git url (this is a mandatory requirement)

## Overview
* `main.py` - the entrypoint. 
* `test_main.py` - basic tests written with Pytest.
* `utils.py` - helper functions.
* `test_utils.py` - basic unit tests for helper functions.
* `models.py` - basic models User, Post and Like for creating and authorizing users, creating posts, making likes and dislikes.
* `db.py` - SQLAlchemy object for easy communication with database.
* `constraints.json` - config file with rules for `bot.py`.
* `bot.py` - separate python script for creating users, posts and making likes accordingly to the rules described in `constraints.json`.
* `requirements.txt` - a list of all project dependencies.

## Requirements
Install the requirements:
```bash
pip3 install -r requirements.txt
```
## Server
Start the server with the following command:  
```bash
FLASK_APP=main python3 -m flask run
```
## Bot
First start the server (follow the instructions above). Then run the bot:
```bash
python3 bot.py
```
## Tests
`test_main.py` can be run using next command:
```bash
python3 -m pytest test/test_main.py
```
`test_utils.py` can be run using next command:
```bash
python3 -m unittest tests/test_utils.py
```
