# bot.py
import json
import requests
import random
from time import sleep

BASE_URL = 'http://127.0.0.1:8000/'


def load_config():
    with open('bot_config.json', 'r') as config_file:
        return json.load(config_file)


def create_users(num_users):
    for i in range(num_users):
        username = f"user_{i}"
        password = "password123"
        data = {
            'username': username,
            'password': password,
        }
        response = requests.post(f"{BASE_URL}signup/", data=data)
        if response.status_code == 201:
            print(f"User {username} created successfully.")
        else:
            print(f"Error creating user {username}. Status code: {response.status_code}")


def create_posts(users, max_posts_per_user):
    for user in users:
        num_posts = random.randint(1, max_posts_per_user)
        for _ in range(num_posts):
            content = f"Post by {user['username']}: {random_post_content()}"
            data = {
                'content': content,
            }
            response = requests.post(f"{BASE_URL}create-post/", data=data, auth=(user['username'], "password123"))
            if response.status_code == 302:
                print(f"Post by {user['username']} created successfully.")
            else:
                print(f"Error creating post by {user['username']}. Status code: {response.status_code}")


def like_posts(users, max_likes_per_user):
    posts = requests.get(f"{BASE_URL}feed/").json()
    for user in users:
        num_likes = random.randint(1, max_likes_per_user)
        for _ in range(num_likes):
            post = random.choice(posts)
            response = requests.post(f"{BASE_URL}post/like/{post['id']}/", auth=(user['username'], "password123"))
            if response.status_code == 201:
                print(f"Post {post['id']} liked by {user['username']}.")
            else:
                print(f"Error liking post {post['id']} by {user['username']}. Status code: {response.status_code}")
        sleep(1)  # Adding a small delay between each like action to simulate more natural behavior


def random_post_content():
    # Replace this with your logic to generate random post content
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit."


def main():
    config = load_config()

    create_users(config["number_of_users"])

    users = [{"username": f"user_{i}", "password": "password123"} for i in range(config["number_of_users"])]

    create_posts(users, config["max_posts_per_user"])

    like_posts(users, config["max_likes_per_user"])


if __name__ == "__main__":
    main()
