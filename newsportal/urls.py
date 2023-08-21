from django.urls import path
from .views import *

urlpatterns = [
    path('news/', ListNews.as_view(), name='news'),
    path('news/search/', ListNews.as_view(), name='news'),
    path('articles/', ListArticles.as_view(), name='articles'),
    path('news/<int:pk>/', DetailNews.as_view(), name='one_news'),
    path('article/<int:pk>/', DetailArticle.as_view(), name='one_article'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),


    path('', index, name='homenewsportal'),
    path('showpost/<int:post_id>', showpost, name='showpost'),
    path('like/<int:post_id>', like_news, name='like'),
    path('dislike/<int:post_id>', dislike_news, name='dislike'),
    path('like-article/<int:post_id>', like_article, name='like_article'),
    path('dislike-article/<int:post_id>', dislike_article, name='dislike_article'),
    path('comments/', comments, name='comments'),
    path('showcomment/<int:comment_id>', showcomment, name='showcomment'),
    path('likecomment/<int:comment_id>', likecomment, name='likecomment'),
    path('dislikecomment/<int:comment_id>', dislikecomment, name='dislikecomment'),
    path('authors/', authors, name='authors'),
]