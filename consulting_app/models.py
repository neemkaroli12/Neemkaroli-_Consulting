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

class Estimate(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    company_name = models.CharField(max_length=200,blank=True,null=True)
    location = models.CharField(max_length=200,blank=True,null=True)
    type = models.CharField(blank=True, null=True)
    Employees_no =  models.IntegerField(blank=True, null=True)
    turnover =     models.IntegerField(blank=True, null=True)
    designation = models.CharField(max_length=200,blank=True,null=True)
    mobile_no = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    existing_appli = models.CharField(max_length=200,blank=True,null=True)
    no_of_users = models.IntegerField(blank=True, null=True)
    product = models.CharField(max_length=200,blank=True,null=True)
    module = models.CharField(max_length=200,blank=True,null=True)