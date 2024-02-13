from django.db.models import Q
from django.views.generic import *
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .utils import *
from django.template.defaultfilters import slugify

class Index(DataMixin, ListView):
    model = Article
    template_name = 'post/index.html'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        page_num = self.request.GET.get('page') or 1
        title = f'Homepage number {page_num}'
        c_def = self.get_data(title = title, page_num = page_num)
        context = super().get_context_data(**kwargs)
        return c_def | context

class AddArticle(PermissionRequiredMixin, DataMixin, CreateView):
    permission_required = 'post.add_post'
    form_class = AddArticleForm
    template_name = 'post/add_article.html'
    
    def get_context_data(self, **kwargs):
        c_def = self.get_data(title = 'Add Article')
        context = super().get_context_data(**kwargs)
        return c_def | context
    
    def get_unique_slug(self, fields):
        slug = slugify(fields.title)
        slug_number = 0
        sorted_articles = Article.objects.filter(slug__contains = slug)
        for article in sorted_articles:
            try:
                if article.slug == slug + '-' + article.slug[len(slug) + 1] or article.slug == slug:
                    slug_number += 1
                    
            except IndexError:
                if article.slug == slug:
                    slug_number += 1
        return slug + '-' + str(slug_number) if slug_number > 0 else slug

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.slug = self.get_unique_slug(fields)
        # print(fields.category.objects.values())
        fields.save()
        return super().form_valid(form)

class ArticleDetail(View):
    def get(self, request, *args, **kwargs):
        view = ArticleDisplay.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = ArticleComment.as_view()
        return view(request, *args, **kwargs)

class ArticleDisplay(DataMixin, DetailView):
    model = Article
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['article'].title
        comment_list = Comment.objects.filter(article = context['article']).order_by('-date')
        category_list = context['article'].category.all()
        form = AddCommentForm()
        c_def = self.get_data(title = title, comment_list = comment_list,
                               category_list = category_list, form = form)
        return c_def | context
    
class ArticleComment(SingleObjectMixin, FormView):
    model = Article
    form_class = AddCommentForm
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(ArticleComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        comment = form.save(commit = False)
        post = self.get_object()
        comment.post = self.object
        comment.article = Article.objects.get(slug = post.slug)
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        post = self.get_object()
        return reverse('article', kwargs = {'slug': post.slug})

class CategoryDetail(DataMixin, DetailView):
    model = Category
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Category.objects.get(slug = context['category'].slug).article_set.all()
        c_def = self.get_data(title = context['category'].name + ' category', article_list = article_list)
        return c_def | context

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'post/register.html'
    success_url = reverse_lazy('signup')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_data(title = 'Sign up')
        return c_def | context

class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'post/login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_data(title = 'Log in')
        return c_def | context
    
class Profile(LoginRequiredMixin, DataMixin, View):
    
    def get(self, request):
        c_def = self.get_data(title = 'Profile')
        context = dict(list(c_def.items()))
        context['comment_list'] = Comment.objects.filter(author = context['user'])
        return render(request, 'post/profile.html', context)

class Search(DataMixin, ListView):
    model = Article
    template_name = 'post/search.html'

    def get_queryset(self):
        query = self.request.GET.get('query').strip()
        return query and Article.objects.filter(Q(title__icontains = query) | Q(content__icontains = query))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query').strip()
        is_empty = not query
        title = 'Empty query' if is_empty else f'Search for {query}'
        c_def = self.get_data(title = title, is_empty = is_empty)
        return c_def | context