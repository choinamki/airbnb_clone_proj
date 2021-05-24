from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error('password', forms.ValidationError('Password is wrong'))
        except models.User.DoesNotExist:
            self.add_error('email', forms.ValidationError('User does not exist'))


class SingUpForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email')

    password = forms.CharField(widget=forms.PasswordInput)
    check_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError('User already exists with the email')
        except models.User.DoesNotExist:
            return email

    def clean_check_password(self):
        password = self.cleaned_data.get('password')
        check_password = self.cleaned_data.get('check_password')

        if password != check_password:
            raise forms.ValidationError('Password confirmation does not match')
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user.username = email
        user.set_password(password)
        user.save()