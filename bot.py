import json
from random import randrange

import requests


with open('constraints.json') as j:
    constraints = json.load(j)

base_url = 'http://127.0.0.1:5000'

users_tokens = []

# Register and login users
for i in range(1, constraints['number_of_users']+1):
    email = 'user' + str(i) + '@example.com'
    password = '12345678'
    response = requests.post(url=base_url + '/users',
                             json={'email': email, 'password': password})
    assert(response.status_code, 200)
    response = requests.post(url=base_url + '/login',
                             json={'email': email, 'password': password})
    assert(response.status_code, 200)
    users_data = response.json()
    users_tokens.append(users_data['token'])

posts_ids = []

# Create posts
for token in users_tokens:
    for i in range(randrange(0, constraints['max_posts_per_user']+1)):
        # create post
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.post(url=base_url + '/posts', json={'text': 'text'},
                                 headers=headers)
        assert(response.status_code, 200)
        posts_ids.append(response.json()['id'])

# Like posts
for token in users_tokens:
    post_ids_temp = posts_ids.copy()
    likes_count = randrange(0, constraints['max_likes_per_user']+1)
    for _ in range(likes_count):
        if len(post_ids_temp) == 0:
            break
        post_id = post_ids_temp[randrange(0, len(post_ids_temp))]
        post_ids_temp.remove(post_id)
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.post(url=base_url + f'/posts/{post_id}/like',
                                 headers=headers)
        assert(response.status_code, 200)
