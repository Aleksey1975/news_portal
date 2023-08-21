from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Sum, Max, Min, Avg, Count
from django.urls import reverse

article = 'a'
news = 'n'
POSTS = (
    (article, 'Статья'),
    (news, 'Новость')
)
class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        if postRat.get('postRating'):
            pRat += postRat.get('postRating')
        commentRat = self.author.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        if commentRat.get('commentRating'):
            cRat += commentRat.get('commentRating')
        self.rating = pRat*3 + cRat
        self.save()

    def __str__(self):
        return self.author.username

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    type_post = models.CharField(max_length=1, choices=POSTS, verbose_name='Тип поста')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ManyToManyField(Category, through="PostCategory", verbose_name='Категория')
    title =  models.CharField(max_length=255, verbose_name='Оглавление')
    content = models.TextField( verbose_name='Содержание')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def get_absolute_url(self):
        return reverse('one_news', args=[str(self.id)])

    def __str__(self):
        return f'{self.get_type_post_display()} - {self.title}'

    def like(self):
        self.rating += 1
    def dislike(self):
        self.rating -= 1
        self.save()
    def  preview(self):
        p = self.content[:124]
        return f'{p}...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
         return f'{str(self.post)} , {str(self.category)}'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'Комментаий к посту {self.post} от пользователя {self.user}'


    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()



# post.category.all()
# category1.post_set.all()
# post1.category.add(category2)
# User.objects.create_user('user5')

