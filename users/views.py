import requests
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms, models
from users.mixins import LoggedOutOnlyView, LoggedInOnlyView, EmailLoginOnlyView


class LoginView(LoggedOutOnlyView, FormView):

    template_name = 'users/login.html'
    form_class = forms.LoginForm

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(self.request, username=email, password=password)
            if user is not None:
                messages.success(self.request, f'Welcome back {user.first_name}')
                login(self.request, user)
                return super().form_valid(form)
        return redirect(reverse('core:home'))

    def get_success_url(self):
        next_arg = self.request.GET.get('next')
        if next_arg is not None:
            return next_arg
        else:
            return reverse('core:home')


def log_out(request):
    messages.success(request, f'See you later {request.user.first_name}')
    logout(request)
    return redirect(reverse('core:home'))


class SignUpView(LoggedOutOnlyView, FormView):
    template_name = 'users/signup.html'
    form_class = forms.SingUpForm
    success_url = reverse_lazy('core:home')

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
    client_id = settings.GH_ID
    redirect_uri = 'http://127.0.0.1:8000/users/login/github/callback'
    return redirect(f'https://github.com/login/oauth/authorize?'
                    f'client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user')


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get('code', None)
        client_id = settings.GH_ID
        client_secret = settings.GH_SECRET
        if code is not None:
            token_request = requests.post(f'https://github.com/login/oauth/access_token?'
                                          f'client_id={client_id}&client_secret={client_secret}&code={code}',
                                          headers={'Accept': 'application/json'})
            token_json = token_request.json()
            error = token_json.get('error', None)
            if error is not None:
                raise GithubException('Can not get access token')
            else:
                access_token = token_json.get('access_token')
                profile_request = requests.get('https://api.github.com/user',
                                               headers={'Authorization': f'token {access_token}',
                                                        'Accept': 'application/json'})
                profile_json = profile_request.json()
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GH:
                            raise GithubException(f'Please log in with: {user.login_method}')
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email, first_name=name, username=email, bio=bio, login_method=models.User.LOGIN_GH
                        )
                        user.set_unusable_password()
                        user.save()
                        login(request, user)
                        messages.success(request, f'Welcome back {user.first_name}')
                    return redirect(reverse('core:home'))
                else:
                    raise GithubException('Can not get your profile')
        else:
            raise GithubException()
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse('core:home'))


def kakao_login(request):
    rest_api_key = settings.KAKAO_API_KEY
    redirect_uri = 'http://127.0.0.1:8000/users/login/kakao/callback'
    return redirect(f'https://kauth.kakao.com/oauth/authorize?'
                    f'client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code')


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        rest_api_key = settings.KAKAO_API_KEY
        redirect_uri = 'http://127.0.0.1:8000/users/login/kakao/callback'
        code = request.GET.get('code')
        token_request = requests.get( f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&'
                                      f'client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}')
        token_json = token_request.json()
        error = token_json.get('error', None)
        if error is not None:
            raise KakaoException('Can not get authorization code.')
        access_token = token_json.get('access_token')
        profile_request = requests.get('https://kapi.kakao.com/v2/user/me',
                                       headers={"Authorization": f"Bearer {access_token}"})
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account").get("email")
        if email is None:
            raise KakaoException('Please also give me your email')
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException('"Please log in with: {user.login_method}')
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = request.get(profile_image)
                user.avatar.save()
                messages.success(request, f'Welcome back {user.first_name}')
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdateProfileView(EmailLoginOnlyView, LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = 'users/update-profile.html'
    fields = ('first_name', 'last_name', 'gender', 'bio', 'birthdate', 'language', 'currency')
    success_message = "Profile Updated"
    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['birthdate'].widget.attrs = {'placeholder': 'Birthdate'}
        form.fields['first_name'].widget.attrs = {'placeholder': 'first_name'}
        form.fields['last_name'].widget.attrs = {'placeholder': 'last_name'}
        return form


class UpdatePasswordView(LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/update-password.html'
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['old_password'].widget.attrs = {'placeholder': 'Current Password'}
        form.fields['new_password1'].widget.attrs = {'placeholder': 'News Password'}
        form.fields['new_password2'].widget.attrs = {'placeholder': 'Confirm new Password'}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session['is_hosting']
    except KeyError:
        request.session['is_hosting'] = True
    return redirect('core:home')
