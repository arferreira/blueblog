from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    owner = models.ForeignKey(User, editable=False)
    title = models.CharField(max_length=500)

    slug = models.CharField(max_length=500, editable=False)



class BlogPost(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=500)
    body = models.TextField()
    shared_to = models.ManyToManyField(Blog, related_name='shared_posts')
    is_published = models.BooleanField(default=False)

    slug = models.SlugField(max_length=500, editable=False)
