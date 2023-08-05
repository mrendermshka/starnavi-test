from django.db import models
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'


def get_posts():
    return Post.objects.all()


import openai
from .models import Post  # Adjust the import path as needed for your app


def post_creator(content, request):
    post = Post()
    openai.api_key = "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"

    try:
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": content
            }]
        )
        post.title = chat_completion.choices[0].message['content']
    except openai.OpenAIError:
        post.title = "Untitled"
    post.content = content
    post.author = request.user if request.user.is_authenticated else None
    post.save()

    return post


def put_like(id, request):
    like = Like()
    like.user = request.user
    like.post = get_object_or_404(Post, id=id)
