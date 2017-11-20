from django import forms
from .models import Post, Comment
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text')

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text',)
        widgets ={
            'text': forms.Textarea(attrs={'rows':1}),
        }

    def clean(self):
        cleaned_data = super(CommentForm,self).clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject and "help" not in subject:
            msg = "Must put 'help' in subject when cc'ing yourself."
            self.add_error('cc_myself', msg)
            self.add_error('subject', msg)



class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder':'Enter name',}))
    subject = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder':'Enter subject for future reference .',}))
    email = forms.CharField(max_length=120, widget=forms.EmailInput(attrs={'placeholder':'Enter valid email id. eg. abc@gmail.com',}))
    message = forms.CharField(widget = forms.Textarea(attrs={'placeholder':'what is in your mind ?',}))
    
