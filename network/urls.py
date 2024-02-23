
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("unfollow", views.unfollow, name="unfollow"),   
    path("follow", views.follow, name="follow"),
    path("removeLike/<int:post_id>", views.removeLike, name="removeLike"),   
    path("like/<int:post_id>", views.like, name="like"), 
    path("edit/<int:post_id>", views.edit, name="edit")   

]
