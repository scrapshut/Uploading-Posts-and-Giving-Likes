from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .models import Post
from django.urls import reverse
from .forms import PostCreateForm, UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def post_list(request):
    pst = Post.published.all()
    query = request.GET.get('q')
    if query:
        pst = Post.published.filter(title=query)
    context = {
        'pst': pst,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, id, slug):
    psts = get_object_or_404(Post, id=id, slug=slug)
    is_liked = False
    if psts.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'psts': psts,
        'is_liked': is_liked,
        'total_likes': psts.total_likes(),
    }
    return render(request, 'posts/post_detail.html', context)


def like_post(request):
    psts = get_object_or_404(Post, id=request.POST.get('psts_id'))
    is_liked = False
    if psts.likes.filter(id=request.user.id).exists():
        psts.likes.remove(request.user)
        is_liked = False
    else:
        psts.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(psts.get_absolute_url())


def post_create(request):
    if request.method=='POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            psts = form.save(commit=False)
            psts.author = request.user
            psts.save()
    else:
        form = PostCreateForm()

    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


def user_login(request):
    if request.method=='POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return HttpResponse("User is inactive")
            else:
                return HttpResponse("User is None")
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('post_list')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('post_list')
    else:
        form=UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/register.html', context)

