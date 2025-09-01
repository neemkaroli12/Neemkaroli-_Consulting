from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def home_two(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def vision(request):
    return render(request, "vision.html")

def leadership(request):
    return render(request, "leadership.html")

def partnership(request):
    return render(request, "partnership.html")

from django.shortcuts import render
from .models import BlogPost

def blog(request):
    # Render the blog listing page
    posts = BlogPost.objects.all()  # Get all blog posts
    return render(request, 'blog.html', {'posts': posts})

def blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    recent_posts = BlogPost.objects.exclude(id=post_id).order_by('-created_at')[:5]
    return render(request, "blog_post.html", {
        "post": post,
        "recent_posts": recent_posts
    })
def implementation(request):
    return render(request, "implementation.html")