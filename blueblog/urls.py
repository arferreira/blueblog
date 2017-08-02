from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from accounts.views import UserRegistrationView
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^new-user/$', UserRegistrationView.as_view(), name='user_registration'),
    url(r'^login/', login, {'template_name': 'base.html'}, name='login'),
]
