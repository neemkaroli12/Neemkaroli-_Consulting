from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .forms import EstimateForm
from .models import BlogPost,Estimate, Module,Product
from django.core.mail import EmailMessage, send_mail
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

from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

def estimate_view(request):
    selected_modules = []  # default empty

    if request.method == 'POST':
        form = EstimateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # 👇 Company type handle karo
            company_type = data['type']
            if company_type.lower() == "other":
                company_type = request.POST.get('other_company_type', company_type)

            # 👇 Existing application handle karo
            existing_app = data['existing_appli']
            if existing_app.lower() == "other":
                existing_app = request.POST.get('other_existing_app', existing_app)

            estimate = Estimate.objects.create(
                name=data['name'],
                company_name=data['company_name'],
                location=data['location'],
                type=company_type,   # 👈 updated
                Employees_no=data['Employees_no'],
                turnover=data['turnover'],
                designation=data['designation'],
                mobile_no=data['mobile_no'],
                email=data['email'],
                existing_appli=existing_app,   # 👈 updated
                no_of_users=data['no_of_users'],
                product=data['product'],
                module=", ".join(request.POST.getlist('module'))
            )

            # Send confirmation email
            subject = "Estimate Submission Confirmation"
            message = (
                f"Hello {estimate.name},\n\n"
                f"Thank you for submitting your estimate request. We will get back to you shortly.\n\n"
                f"Details:\nCompany: {estimate.company_name}\n"
                f"Product: {estimate.product}\n"
                f"Modules: {estimate.module}\n\nBest Regards,\nYour Company"
            )
            recipient_list = [estimate.email]

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            return render(request, 'success.html')  # or redirect

        else:
            # If form invalid, keep selected modules to re-populate checkboxes
            selected_modules = request.POST.getlist('module')

    else:
        form = EstimateForm()

    return render(request, 'estimate_form.html', {
        'form': form,
        'selected_modules': selected_modules,
    })

def get_modules(request):
    product_id = request.GET.get('product_id')
    modules = []

    try:
        if not product_id:  
            # Agar product select hi nahi hua -> unlinked modules dikhao
            modules = list(Module.objects.filter(product__isnull=True).values('id', 'name'))
        else:
            product = Product.objects.get(id=product_id)
            if product.name == "NA":
                modules = list(Module.objects.filter(product__isnull=True).values('id', 'name'))
            else:
                modules = list(product.modules.values('id', 'name'))
    except Product.DoesNotExist:
        modules = []

    return JsonResponse(modules, safe=False)


def odoo_imple(request):
    return render(request,'odoo_imple.html')

def odoo_support(request):
    return render(request,'odoo_support.html')

def odoo_consulting(request):
    return render(request,'odoo_consulting.html')