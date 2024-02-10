from django import forms
from .models import Comment, Post


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]

