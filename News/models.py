from django.contrib.auth.forms import UserCreationForm
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

# Create your models here.

class Author(models.Model):
    auth_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        sum_posts_rating = self.post_set.all().aggregate(Sum('post_rating'))['post_rating__sum']*3
        sum_comments = self.id_user.comment_set.all().aggregate(Sum('comment_rating'))['comment_rating__sum']
        sum_comments_post = self.post_set.all().aggregate(Sum('comment__comment_rating'))['comment__comment_rating__sum']
        #result_rating
        self.rating = sum_posts_rating + sum_comments + sum_comments_post
        self.save()

    def __str__(self):
        return f'{self.user.username}'

class Category(models.Model):

    category_name = models.CharField(max_length=255, unique = True, null=True, blank=True)

    def __str__(self):
       return self.category_name

article = 'ART'
news = 'NEW'
CHOICES = [(article, 'Статья'),
        (news, 'Новость')]

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add = True)
    post_type = models.CharField(max_length=3, choices = CHOICES, default = news)
    title = models.CharField(max_length=255)
    content = models.TextField()
    post_rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through = 'PostCategory')

    def categoria(self):
        for categ in self.category.all():
            return categ


    def preview(self):
        return self.content[:124] + '...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.category.all()} : {self.author} : {self.title}: {self.content[:35]}: rating = {self.post_rating}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.category.category_name} : {self.post.id}'




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=300)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_text}: {self.comment_time} {self.comment_rating}'

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
