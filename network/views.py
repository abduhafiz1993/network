from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# from this folder imported code 
from .models import User
from .form import *

# paginator
from django.core.paginator import Paginator

def index(request):
    allposts = Post.objects.all().order_by("timestamp").reverse()

    posts = Paginator(allposts, 10)
    pageNumber = request.GET.get('page')
    page_obj = posts.get_page(pageNumber) 
    
    return render(request, "network/allpost.html",{
        "page_obj" : page_obj
    })


def newpost(request):
    form = NewPost()
    if request.method == "POST":
        form = NewPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.like = 0
            post.save()
            return redirect('index')
            
    return render(request, "network/index.html", {
        'form': form
        })

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allposts = Post.objects.filter(user=user).order_by("timestamp").reverse()

    posts = Paginator(allposts, 10)
    pageNumber = request.GET.get('page')
    page_obj = posts.get_page(pageNumber) 
    
    return render(request, "network/allpost.html",{
        "page_obj" : page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def following(request):
    pass