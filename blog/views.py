from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView
from django.views.generic import TemplateView

# importando o form para criação do Blog
from blog.forms import BlogForm

# importando forbidden para barrar a criação do blog a 1
from django.http.response import HttpResponseForbidden
# importando o model blog
from blog.models import Blog

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
                ctx['blog'] = Blog.objects.filter(owner=self.request.user).last()
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
