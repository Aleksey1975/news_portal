from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView


class ListPosts(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'newsportal/index_news.html'
    context_object_name = 'news'


class ListDetail(DetailView):
    model = Post
    template_name = 'newsportal/one_news.html'
    context_object_name = 'news'



def index(request):
    posts = Post.objects.order_by('-rating')
    best_post = posts[0]
    context = {
        'title':'News Portal',
        'posts':posts,
        'best_post':best_post

    }
    return render(request, 'newsportal/index.html', context)

def showpost(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        'title':post.title,
        'post':post

    }
    return render(request, 'newsportal/showpost.html', context)

def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.like()
    post.save()
    return redirect('showpost', post_id)

def dislike(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.dislike()
    post.save()
    return redirect('showpost', post_id)

def comments(request):
    comments = Comment.objects.all()
    context = {
        'title':'Comments',
        'comments':comments
    }
    return render(request, 'newsportal/comments.html', context)


def showcomment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    context = {
        'title':'comment',
        'comment':comment

    }
    return render(request, 'newsportal/showcomment.html', context)


def likecomment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.like()
    comment.save()
    return redirect('showcomment', comment_id)

def dislikecomment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.dislike()
    comment.save()
    return redirect('showcomment', comment_id)


def authors(request):
    users = User.objects.all()
    aus = Author.objects.order_by('-rating')
    the_best = aus[0]
    for a in aus:
        a.update_rating()
        a.save()

    context = {
        'title':'Authors',
        'authors':aus,
        'best':the_best,

    }
    return render(request, 'newsportal/authors.html', context)
