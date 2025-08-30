from django.db import models
from django.utils import timezone   

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)   # fix
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

