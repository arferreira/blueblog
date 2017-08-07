from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from accounts.views import UserRegistrationView
from django.contrib.auth.views import login, logout
# importando view para criação, home e edição do blog
from blog.views import NewBlogView, HomeView, UpdateBlogView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^new-user/$', UserRegistrationView.as_view(), name='user_registration'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/login/'}, name='logout'),
    url(r'^blog/new/$', NewBlogView.as_view(), name='new-blog'),
    url(r'^blog/(?P<pk>\d+)/update/$', UpdateBlogView.as_view(), name='update-blog'),

]
