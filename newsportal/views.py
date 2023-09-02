from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import *
from .filters import *
from .forms import *
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

class ListNews(ListView):
    queryset = Post.objects.filter(type_post=news)
    ordering = '-time_created'
    template_name = 'newsportal/index_news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class ListArticles(ListView):
    queryset = Post.objects.filter(type_post=article)
    ordering = '-time_created'
    template_name = 'newsportal/index_articles.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class DetailNews(DetailView):
    model = Post
    template_name = 'newsportal/one_news.html'
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['author1'] = str(post.author)
        context['admin'] = 'admin'

        return context


class DetailArticle(DetailView):
    model = Post
    template_name = 'newsportal/one_article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['author1'] = str(post.author)
        context['admin'] = 'admin'

        return context

class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'newsportal/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = 'Добавить новость'
        context['button'] = 'Добавить'
        context['title'] = 'Добавить новость'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = news
        return super().form_valid(form)



class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'newsportal/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = 'Добавить статью'
        context['button'] = 'Добавить'
        context['title'] = 'Добавить статью'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = article
        return super().form_valid(form)



class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'newsportal/post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if str(post.author) != str(self.request.user):
            return HttpResponse("Доступ eзапрещен!")
        return super(NewsEdit, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отредактировать новость'
        context['button'] = 'Отредактировать'
        return context

class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'newsportal/post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if str(post.author) != str(self.request.user):
            return HttpResponse("Доступ eзапрещен!")
        return super(ArticleEdit, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = 'Отредактировать статью'
        context['button'] = 'Отредактировать'
        return context

class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'newsportal/news_delete.html'
    success_url = reverse_lazy('news')


class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'newsportal/article_delete.html'
    success_url = reverse_lazy('articles')

def index(request):
    posts = Post.objects.order_by('-rating')
    best_post = posts[0]
    context = {
        'title':'Все посты',
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

def like_news(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.like()
    post.save()
    return redirect('one_news', post_id)

def dislike_news(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.dislike()
    post.save()
    return redirect('one_news', post_id)

def like_article(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.like()
    post.save()
    return redirect('one_article', post_id)

def dislike_article(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.dislike()
    post.save()
    return redirect('one_article', post_id)

def comments(request):
    comments = Comment.objects.all()
    context = {
        'title':'Комментарии',
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
        'title':'Авторы',
        'authors':aus,
        'best':the_best,

    }
    return render(request, 'newsportal/authors.html', context)
