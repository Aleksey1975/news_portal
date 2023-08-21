from django.urls import path
from .views import *

urlpatterns = [
    path('news/', ListPosts.as_view(), name='news'),
    path('news/<int:pk>/', ListDetail.as_view(), name='one_news'),

    path('', index, name='homenewsportal'),
    path('showpost/<int:post_id>', showpost, name='showpost'),
    path('like/<int:post_id>', like, name='like'),
    path('dislike/<int:post_id>', dislike, name='dislike'),
    path('comments/', comments, name='comments'),
    path('showcomment/<int:comment_id>', showcomment, name='showcomment'),
    path('likecomment/<int:comment_id>', likecomment, name='likecomment'),
    path('dislikecomment/<int:comment_id>', dislikecomment, name='dislikecomment'),
    path('authors/', authors, name='authors'),
]