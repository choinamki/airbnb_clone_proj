from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

import config.settings
from . import forms, models


class LoginView(FormView):

    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(self.request, username=email, password=password)
            if user is not None:
                login(self.request, user)
                return super().form_valid(form)
        return redirect(reverse('core:home'))


def log_out(request):
    logout(request)
    return redirect(reverse('core:home'))


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = forms.SingUpForm
    success_url = reverse_lazy('core:home')
    initial = {
        'first_name': 'Choi',
        'last_name': 'Namki',
        'email': 'test@gmail.com',
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ''
        user.save()
        # to do: add succes message
    except models.User.DoesNotExist:
        # to do : add error message
        pass
    return redirect(reverse('core:home'))


def github_login(request):
    client_id = settings.json_data['gh_id']
    redirect_uri = 'http://127.0.0.1:8000/users/login/github/callback'
    return redirect(f'https://github.com/login/oauth/authorize? \
                    client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user')


def github_callback(reuqest):
    oass