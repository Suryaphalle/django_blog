from django import forms
from .models import Post, Comment
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Post Title'}),            
        }

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text',)
        widgets ={
            'text': forms.Textarea(attrs={'rows':1, 'placeholder':'Write your thoughts about post.'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder':'Enter name',}))
    subject = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder':'Enter subject for future reference.',}))
    email = forms.CharField(max_length=120, widget=forms.EmailInput(attrs={'placeholder':'Enter valid email id. eg. abc@gmail.com',}))
    message = forms.CharField(widget = forms.Textarea(attrs={'placeholder':'what is in your mind ?',}))
    
class RequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write Your Message Here',}))    