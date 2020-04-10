from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User as Users
from django.http import HttpResponse

from .models import *
from .utils import *
from .forms import TagForm, PostForm, UserRegistrationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.db.models import Q

import datetime


from django.contrib.auth import models

# group = models.Group.objects.get(name='blogger')
# users = group.user_set.all()

def posts_list(request):
    search_querry = request.GET.get('search','')

    if search_querry:
        posts = Post.objects.filter(Q(title__icontains=search_querry) | Q(body__icontains=search_querry))
    else:
        posts = Post.objects.all()

    new = False

    for post in posts:
        post_list = list(str(post.date_pub))
        time_now_list = list(str(datetime.date.today()))
        for i in range(22):
            del post_list[-1]
        for i in range(8):
            del post_list[0]
            del time_now_list[0]
        if post_list[0] == "0":
            del post_list[0]
        if time_now_list[0] == "0":
            del time_now_list[0]
        text_p = ""
        for el in post_list:
            text_p += el
        text_n = ""
        for el in time_now_list:
            text_n += el
        if int(text_p) <= int(text_n):
            new = True
        else:
            new = False

    user_id = request.user.id
    print()
    print()
    print(user_id)
    print()
    print()

    context = {
        'posts': posts,
        'new': new,
        'user_id': user_id,
    }

    return render(request, 'blog/index.html', context=context)

# def contact(request):
#     return render(request, 'blog/news_detail.html')

def profiles_detail(request):
    users = Users.objects.all()
    return render(request, 'blog/profiles_detail.html', context={"users": users})

def profile_detail(request, id):
    user_id = id
    id_this_user = request.user.id
    name_user = Users.objects.filter(id=user_id)
    name_this_user = Users.objects.filter(id=id_this_user)

    message_token = (user_id + id_this_user) * 37127

    if int(id_this_user) == int(user_id):
        my_acc = True
    else:
        my_acc = False

    context = {
        'id_this_user':id_this_user,
        'user_id':user_id,
        'name_user':name_user,
        'message_token':message_token,
        'my_acc':my_acc,
    }

    return render(request, 'blog/profile_detail.html', context=context)

def message_detail(request):
    return render(request, 'blog/message_detail.html')

def chat_detail(request, message_token):
    id_chat = message_token
    messages = MessageChat.objects.filter(message_id=id_chat)

    if request.method == "POST":
        MessageChat.objects.create(body = request.POST['name'], message_id=id_chat)

    return render(request, 'blog/chat_detail.html', context={'id_chat':id_chat, 'messages':messages})

class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin,ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
