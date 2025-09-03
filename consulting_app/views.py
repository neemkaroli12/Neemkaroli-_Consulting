from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import CareerApplicationForm

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
    posts = BlogPost.objects.all() 
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

def cons(request):
    return render(request,"consulting.html")

def support(request):
    return render(request,"micro_support.html")
    
def career(request):
    if request.method == "POST":
        form = CareerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            resume = form.cleaned_data.get('resume')

            email_subject = f"New Career Application from {name}"
            email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            email_message = EmailMessage(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                ['neemkaroligroup@gmail.com'],  # Change to your recipient email
                reply_to=[email],
            )

            if resume:
                email_message.attach(resume.name, resume.read(), resume.content_type)

            email_message.send()

            return render(request, 'career.html', {
                'form': CareerApplicationForm(),  # reset form
                'success': True,
                'applicant_name': name
            })

    else:
        form = CareerApplicationForm()

    return render(request, 'career.html', {'form': form})

def micro_service(request):
    return render(request, "micro_service.html")

def odoo_service(request):
    return render(request,'odoo_Professional.html')

def odoo_upgrade(request):
    return render(request,'odoo_upgrade.html')