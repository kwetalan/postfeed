from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name = 'home'),
    path('addarticle', AddArticle.as_view(), name = 'addarticle'),
    path('signup', RegisterUser.as_view(), name = 'signup'),
    path('login', LoginUser.as_view(), name = 'login'),
    path('profile', Profile.as_view(), name = 'profile'),
    path('article/<slug:slug>', ArticleDetail.as_view(), name = 'article'),
    path('category/<slug:slug>', CategoryDetail.as_view(), name = 'category'),
    path('search/', Search.as_view(), name='search'),
]
