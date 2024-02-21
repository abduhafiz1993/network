from django.contrib.auth.models import AbstractUser
from django.db import models

## user class
class User(AbstractUser):
    pass


##  post model
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    # like have many to many relation to user 
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Content: {self.content} likes: {self.likes.length()}"

class Comment(models.Model):
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Text: {self.text} comment_time: {self.comment_time} commenter:{self.commenter} auction_listing: {self.auction_listing}"


class Follow(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name = 'user_is_following')
    user_follower = models.ForeignKey(user, on_delete=models.CASCADE, related_name ='user_being_followed')
    


    def __str__(self):
        return f"{self.user} is following {self.user_follower}"