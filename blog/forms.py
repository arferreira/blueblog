from django import forms
from blog.models import Blog, BlogPost

# Form para criação do Blog pai
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title'
        ]

# Form para criação dos posts dos blogs
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost

        fields = [
            'title',
            'body'
        ]
