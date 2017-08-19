from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext as _

from account.models import User


PASSWORD_DONT_MATCH = _("Passwords don't match!")


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_check = forms.CharField(label='Password Confirmation',
                                     widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name')

    def clean_password_check(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')
        if password and password_check and password != password_check:
            raise forms.ValidationError(PASSWORD_DONT_MATCH)
        return password

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'name', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
