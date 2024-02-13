from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.TextField()
    slug = models.SlugField(db_index=True)
    content = models.TextField()
    image = models.ImageField(upload_to='', blank=True, null=True)
    category = models.ManyToManyField('Category', blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/article/{self.slug}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/category/{self.slug}'
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'

    class Meta:
        verbose_name = 'Комент'
        verbose_name_plural = 'Коменты'
