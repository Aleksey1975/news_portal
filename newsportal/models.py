from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Sum, Max, Min, Avg, Count

article = 'a'
news = 'n'
POSTS = (
    (article, 'article'),
    (news, 'news')
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
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=1, choices=POSTS)
    time_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title =  models.CharField(max_length=255)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)

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
        return self.post , self.category



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


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

