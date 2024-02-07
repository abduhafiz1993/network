from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Content: {self.content} likes: {self.likes}"

class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    Post_List = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Text: {self.text} comment_time: {self.comment_time} commenter:{self.commenter} auction_listing: {self.auction_listing}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)



User.profile = property(lambda u: UserProfile.objects.get_or_create(user = u)[0])
