from django.urls import path
from .views import *

urlpatterns = [
    # path('', redirect_to_page),
    path('main/', main_view, name='main'),
    path('signup/', register_process, name='user-signup-api'),
    path('login/', login_process, name='user-login-api'),
    path('logout/', logout_process, name='user-logout'),
    path('feed/', feed, name='feed-page'),
    path('create-post', create_post_process, name='post-creator'),
    path('post/like/<id>/', like_post, name='post-like'),
    path('signup-page/', register_page, name='user-signup-page'),
    path('login-page/', login_page, name='user-login-page'),
    path('api/analitics/', like_analytics, name='like_analytics'),
]
