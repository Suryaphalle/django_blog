# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from blog.utils import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.views.generic import View
from blog.models import Post
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('registration/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request,'registration/account_activation_sent.html')


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active =True
        user.profile.email_confirmed = True
        user.save()
        login(request,user)
        return redirect('home')
    else:
        return render(request,'registration/account_activation_invalid.html')   


class MyProfileView(View):
    model =User
    template_name = 'registration/my_profile.html'
    context_object_name = 'user_posts'
    paginate_by = 10

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{'user_posts': self.context_object_name})

def validate_username(request):
    username = request.GET.get('username',None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['errorMessage'] = 'A user with this username already exists.'
    return JsonResponse(data)