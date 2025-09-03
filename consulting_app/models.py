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


class CompanyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Module(models.Model):
    product = models.ForeignKey(Product, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.product.name})"


class Estimate(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    type = models.ForeignKey(CompanyType, on_delete=models.SET_NULL, null=True, blank=True)
    Employees_no = models.IntegerField(blank=True, null=True)
    turnover = models.IntegerField(blank=True, null=True)
    designation = models.CharField(max_length=200, blank=True, null=True)
    mobile_no = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField()
    existing_appli = models.CharField(max_length=200, blank=True, null=True)
    no_of_users = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    module = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.company_name}"
    
class Branch(models.Model):
    estimate = models.ForeignKey(Estimate, related_name='branches', on_delete=models.CASCADE)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.location} ({self.estimate.company_name})"