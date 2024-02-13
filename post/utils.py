from post.forms import SearchForm
from .models import Category
from django.db.models import Count
from uuid import uuid4

class DataMixin():
    def get_data(self, **kwargs):
        context = kwargs
        context['cats'] = Category.objects.annotate(article_count = Count('article')).order_by('-article_count')
        context['search_form'] = SearchForm()
        context['is_admin'] = self.request.user.is_superuser
        context['is_auth'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context