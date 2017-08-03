from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import CreateView

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
