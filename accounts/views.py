from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.views.generic import CreateView

# Classe de registro de usuário

class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_registration.html'

    def get_success_url(self):
        return reverse('home')
