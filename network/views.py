from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse
##
import json
from django.http import JsonResponse
# from this folder imported code 
from .models import *
from .form import *

# paginator
from django.core.paginator import Paginator

def edit(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})


def index(request):
    allposts = Post.objects.all().order_by("timestamp").reverse()

    posts = Paginator(allposts, 10)
    pageNumber = request.GET.get('page')
    page_obj = posts.get_page(pageNumber) 
    
    return render(request, "network/allpost.html", {
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
    userame = user.username
    allposts = Post.objects.filter(user=user).order_by("timestamp").reverse()

    following = Follow.objects.filter(user = user)
    follower = Follow.objects.filter(user_follower = user)

    try:
        checkFollow = follower.filter(user=User.objects.get(pk=request.user.pk)) 
        if len (checkFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    posts = Paginator(allposts, 10)
    pageNumber = request.GET.get('page')
    page_obj = posts.get_page(pageNumber) 
    
    return render(request, "network/profile.html",{
        "page_obj" : page_obj,
        "username" : userame,
        "follower" : follower,
        "following" : following,
        "isFollowing" : isFollowing,
        "user_profile" : user
    })

def follow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk = request.user.pk)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow(user=currentUser, user_follower=userfollowData)
    f.save()
    user_id = userfollowData.pk
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


def unfollow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk = request.user.pk)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow.objects.filter(user=currentUser, user_follower=userfollowData)
    f.delete()
    user_id = userfollowData.pk
    return redirect(reverse('profile', kwargs={'user_id': user_id}))

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
    currentUser = User.objects.get(pk=request.user.pk)
    followingPeople = Follow.objects.filter(user=currentUser)
    allposts = Post.objects.all().order_by("timestamp").reverse()

    followingPosts = []

    for post in allposts:
        for person in followingPeople:
            if person.user_follower == post.user:
                followingPosts.append(post)


    posts = Paginator(followingPosts, 10)
    pageNumber = request.GET.get('page')
    page_obj = posts.get_page(pageNumber) 
    
    return render(request, "network/following.html", {
        "page_obj" : page_obj
    })            