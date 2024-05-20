from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")


    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
    


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(required=False)
    date_joined = forms.DateTimeField(required=False)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email']  # Lisää tähän kaikki kentät, jotka haluat säilyttää lomakkeessa



class PasswordCheckForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="Nykyinen salasana")