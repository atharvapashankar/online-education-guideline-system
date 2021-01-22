from django.forms import ModelForm, Textarea, TextInput
from .models import Review
from django import forms
from django.contrib.auth.models import User


# Form to take display to take user's review
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        #user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'abcd'}))
        widgets = {
            'comment' : Textarea(attrs={'cols':35, 'rows':10}),
            #'user_name' : TextInput(attrs={'placeholder':User.username,})

        }

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'forminput'}))
    password = forms.CharField(widget=forms.PasswordInput)


