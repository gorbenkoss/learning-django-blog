from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_public']
        widgets = {
            'is_public': forms.CheckboxInput()
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=10, help_text=_('Required. 10 characters or fewer. Letters, digits and @/./+/-/_ only.'))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
        