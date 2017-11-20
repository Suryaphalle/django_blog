    # -*- coding: utf-8 -*-

import operator
from django.db.models import Q, F, Count, IntegerField
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from .models import Post, Comment
from .forms import PostForm, CommentForm, ContactForm
from accounts.forms import SignUpForm
import json

from .mixins import AjaxFormMixin
# Create your views here.


def home(request):
    posts = Post.objects.all()[:5]
    return render(request,'blog/post_list.html',{'posts':posts}) 

def post_list(request):
    post_list = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    # post_list = Post.objects.all()
    page = request.GET.get('page',1)

    paginator = Paginator(post_list,4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render (request,'blog/post_list.html',{'posts':posts})
   # return render(request, 'blog/post_list.html',{'posts': posts})


def post_detail(request,pk):
    post = get_object_or_404(Post, pk = pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post':post,'form':form} )

@login_required
def post_new(request):
    if request.is_ajax:    
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return JsonResponse('posted successfully ',safe=False)
        else:
            form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,instance = post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date= timezone.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm(instance = post)
    return render(request,'blog/post_edit.html',{'form':form})

@login_required
def del_blog(request,pk):
    post = get_object_or_404(Post,pk=pk)
    #form = PostForm(instance = post)
    post.delete()
    messages.success(request, 'Blog: {} Deleted.'.format(post.title))
    # return render(request,'blog/post_list.html',{'post':post})
    return redirect('post_list')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request,'Please correct the error below.')
            return render(request,'blog/change_password.html',{'form':form})

    else:
        form = PasswordChangeForm(request.user)
    return render(request,'blog/change_password.html',{'form':form})

def user_list(request):
    user_list = User.objects.all()
    page = request.GET.get('page',1)

    paginator = Paginator(user_list,2)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render (request,'blog/user_list.html',{'users':users})

def add_comment_to_post(request,pk):
    post =get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html',{'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


class AboutView(TemplateView):
    template_name = 'about_us.html'

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self,**kwargs):
        queryset = Post.objects.all()
        context = super(HomeView,self).get_context_data(**kwargs)
        return context

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    paginate_by = 3
    queryset = Post.objects.all()

    def get_context_data(self,**kwargs):
        queryset = Post.objects.all()
        context = super(PostListView,self).get_context_data(**kwargs)
        context['most_views_posts'] = queryset.order_by('-views')[:5]
        context['updated_posts'] = queryset.order_by('-updated_date')[:5]
        posts_objects = Post.objects.annotate(num_comments=Count('comments'))
        context['most_commented'] = posts_objects.order_by('-num_comments')[:5]
        return context

    def get_queryset(self):
        queryset = super(PostListView,self).get_queryset()
        query = self.request.GET.get('q')

        if query is not None:
            queryset = Post.objects.search(query)
            return queryset

        return queryset

class PostDetailView(DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def get_context_data(self,**kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        context['post_detail'] = Post.objects.all()
        return context

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.form_class()
        session_key = 'viewed_post_{}'.format(self.object.pk)
        if not request.session.get(session_key,False):
            self.object.views = F('views')+1
            self.object.save()
            request.session[session_key]=True

        return render(request, self.template_name, {'form': form, 'post': self.object})

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.form = self.form_class(request.POST)
        if request.is_ajax():
                try:
                    parent_id = self.request.POST.get('parent_id')
                except:
                    parent_id = None

                if self.form.is_valid():
                    comment = self.form.save(commit=False)
                    comment.author = self.request.user
                    comment.post = self.object

                    if parent_id is not None:
                        parent = get_object_or_404(Comment,pk=parent_id)
                        comment.parent = parent
                        self.form.save()
                    self.form.save()
                    data = {
                        'message' : 'Successfully submitted comment data.'
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'message': 'errors.'
                    }
                    return JsonResponse(data)
            #    return redirect('post_detail',pk=self.object.pk)
            # else:
            #     return self.render(request)
            # # return render(request, self.template_name, {'form': self.form, 'post': self.object})
    

class ContactView(FormView,AjaxFormMixin):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self,form):
        response = super(ContactView,self).form_valid(form)
        if self.request.is_ajax():

                name = form.cleaned_data['name']
                subject = form.cleaned_data['subject']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']
                send_email(subject,message,email,['admin@example.com'])
                data = {
                   'message': 'Successfully submitted data.'
                }
                return JsonResponse(data)
        else:
                return response

    def form_invalid(self,form):
        response = super(AjaxFormMixin,self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors,status=400)
        else:
            return response



class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def form_valid(self,form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super(PostCreateView, self).form_valid(form)
    # def form_valid(self,form):
    #     form.instance.author = self.request.user
        
    #     response = super(PostCreateView, self).form_valid(form)
    #     if self.request.is_ajax():
    #         instance = form.save()
    #         instance.save()
    #         data = {
    #            'message': 'Successfully submitted post.'
    #         }
    #         return JsonResponse(data)
    #     else:
    #         return response

    # def form_invalid(self,form):
    #     response = super(PostCreateView,self).form_invalid(form)
    #     if self.request.is_ajax():
    #         data = {
    #            'message': 'forms errors.'
    #         }
    #         return JsonResponse(data,form.errors,status=400)
    #     else:
    #         return response

    def get_context_data(self,**kwargs):
        context = super(PostCreateView,self).get_context_data(**kwargs)
        context['title_text'] = 'New Post'
        context['btn_text'] = 'Create Post'
        return context



class PostUpdateView(UpdateView,AjaxFormMixin):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super(PostUpdateView, self).form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(PostUpdateView,self).get_context_data(**kwargs)
        context['title_text'] = 'Edit Post'
        context['btn_text'] = 'Update Post'
        return context


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'blog/conferm_del.html'
    success_url = reverse_lazy('post_list')


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super(SignUpView,self).form_valid(form)

    def form_invalid(self,form):
        return super(SignUpView,self).form_invalid(form)

# class BlogSearchListView(ListView):
#     model = Post
#     paginate_by = 10
#     template_name = 'blog/post_list.html'
#     context_object_name = 'posts'
#     queryset = Post.objects.all()


        # if query:
        #     query_list = query.split()
        #     queryset = queryset.filter(reduce(operator.and_,(Q(title__icontains=q) for q in query_list)) |
        #         reduce(operator.and_,(Q(text__icontains=q) for q in query_list))
        #     )
        # return queryset
def search_post_title(request):
    if request.is_ajax:
        title = request.GET.get('start','')
        post = Post.objects.all().filter(Q(title__icontains=title))
        results = []
        for post_title in post:
            post_title_json = {}
            post_title_json['label']= post_title.title
            post_title_json['value']= post_title.title
            results.append(post_title_json)
        data_json = json.dumps(results)
    else:
        data_json = 'fail'
    return HttpResponse(data_json,content_type='application/json')

# class PostLikeToggle(RedirectView):
#     def get_redirect_url(self,*args,**kwrgs):
#         pk = self.kwargs.get("pk")
#         print(pk)
#         obj = get_object_or_404(Post, pk=pk)
#         url_ = obj.get_absolute_url()
#         user = self.request.user
#         if user.is_authenticated():
#             if user in obj.likes.all():
#                 obj.likes.remove(user)
#             else:
#                 obj.likes.add(user)
#         return url_

