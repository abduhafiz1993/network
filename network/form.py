from django import forms
from .models import Comment, Post


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = [""]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
