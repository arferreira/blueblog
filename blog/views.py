from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView
from django.views.generic import TemplateView, DetailView

# importando o form para criação do Blog
from blog.forms import BlogForm
# Importando o form para criação de post
from blog.forms import BlogPostForm
# importando forbidden para barrar a criação do blog a 1
from django.http.response import HttpResponseForbidden
# importando o model blog
from blog.models import Blog
# importando o model para post de blog
from blog.models import BlogPost

# barrar o acesso a usuário não logado e anonimo
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class NewBlogView(CreateView):
    form_class = BlogForm
    template_name = 'blog_settings.html'

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.owner = self.request.user
        blog_obj.slug = slugify(blog_obj.title)

        blog_obj.save()
        return HttpResponseRedirect(reverse('home'))
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if Blog.objects.filter(owner=user).exists():
            return HttpResponseForbidden('Você não pode criar mais de um blog')
        else:
            return super(NewBlogView, self).dispatch(request, *args, **kwargs)

# definindo a home da app
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            if Blog.objects.filter(owner=self.request.user).exists():
                ctx['has_blog'] = True
                blog = Blog.objects.filter(owner=self.request.user).last()
                ctx['blog'] = blog
                ctx['blog_posts'] = BlogPost.objects.filter(blog=blog)
        return ctx



# definindo a view de edição do blog
class UpdateBlogView(UpdateView):
    form_class = BlogForm
    template_name = 'blog_settings.html'
    success_url = '/'
    model = Blog

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogView, self).dispatch(request, *args, **kwargs)

# definindo view para Posts do Blog
class NewBlogPostView(CreateView):
    form_class = BlogPostForm
    template_name = 'blog_post.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewBlogPostView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        blog_post_obj = form.save(commit=False)
        blog_post_obj.blog = Blog.objects.get(owner=self.request.user)
        blog_post_obj.slug = slugify(blog_post_obj.title)
        blog_post_obj.is_published = True

        blog_post_obj.save()

        return HttpResponseRedirect(reverse('home'))

# definindo a view de edição dos posts do blog
class UpdateBlogPostView(UpdateView):
    form_class = BlogPostForm
    template_name = 'blog_post.html'
    success_url = '/'
    model = BlogPost

    def get_queryset(self):
        queryset = super(UpdateBlogPostView, self).get_queryset()
        return queryset.filter(blog__owner=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogPostView, self).dispatch(request, *args, **kwargs)

# definindo a view para visualizar os detalhes do post
class BlogPostDetailsView(DetailView):
    model = BlogPost
    template_name = 'blog_post_details.html'
