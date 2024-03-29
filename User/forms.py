from django import forms
from . models import NewUser, Transfer
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
#from captcha.fields import CaptchaField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    #captcha = CaptchaField()
    class Meta:
        model = NewUser
        fields = '__all__'
     
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SignUpForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ['email', 'phone', 'first_name', 'last_name', 'password1', 'password2']
