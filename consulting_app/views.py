from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import EstimateForm
from .models import BlogPost,Estimate, Branch,Product,Module,SubModule,SubSubModule
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .forms import CareerApplicationForm
from django.views.decorators.csrf import csrf_exempt
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
from django.http import JsonResponse

def estimate_view(request):
    selected_modules = []
    selected_submodules = []
    selected_subsubmodules = []
    estimate = None

    if request.method == 'POST':
        form = EstimateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Modules
            selected_modules = request.POST.getlist("modules")
            for mid in selected_modules:
                sub_list = request.POST.getlist(f"submodules_{mid}")
                selected_submodules.extend(sub_list)
                for sid in sub_list:
                    subsub_list = request.POST.getlist(f"subsubmodules_{sid}")
                    selected_subsubmodules.extend(subsub_list)

            # Cost Estimation
            total_functional_days = 0
            total_technical_days = 0
            modules = Module.objects.filter(id__in=selected_modules)
            for m in modules:
                total_functional_days += m.functional_days or 0
                total_technical_days += m.technical_days or 0

            functional_cost = total_functional_days * 900
            technical_cost = total_technical_days * 800
            final_cost = functional_cost + technical_cost

            # Save Estimate
            estimate = Estimate.objects.create(
                name=data['name'],
                company_name=data['company_name'],
                location=data['location'],
                type=data['type'],
                Employees_no=data['Employees_no'],
                turnover=data['turnover'],
                designation=data['designation'],
                mobile_no=data['mobile_no'],
                email=data['email'],
                existing_appli=data['existing_appli'],
                no_of_users=data['no_of_users'],
                product=data['product'],
                module=", ".join(selected_modules),
                submodules=", ".join(selected_submodules),
                subsubmodules=", ".join(selected_subsubmodules),
                functional_days=total_functional_days,
                technical_days=total_technical_days,
                functional_cost=functional_cost,
                technical_cost=technical_cost,
                final_cost=final_cost,
            )

            # Branch save
            branches = data.get('branches', "")
            if branches:
                for loc in [b.strip() for b in branches.split(",") if b.strip()]:
                    Branch.objects.create(estimate=estimate, location=loc)

            # Confirmation Email
            subject = "Estimate Submission Confirmation"
            message = (
                f"Hello {estimate.name},\n\n"
                f"Thank you for submitting your estimate request.\n\n"
                f"Company: {estimate.company_name}\n"
                f"Product: {estimate.product}\n"
                f"Modules: {estimate.module}\n"
                f"SubModules: {estimate.submodules}\n"
                f"SubSubModules: {estimate.subsubmodules}\n\n"
                f"Total Estimate: ₹{final_cost}\n\n"
                f"Best Regards,\nYour Company"
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [estimate.email])

            # 🔹 Ajax response
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "final_cost": final_cost,
                })

    else:
        form = EstimateForm()

    return render(request, 'estimate_form.html', {"form": form})

    
@csrf_exempt
def calculate_estimate(request):
    if request.method == "POST":
        modules = request.POST.getlist("modules")

        total_functional_days = 0
        total_technical_days = 0

        # Modules ke functional + technical days add karna
        for mid in modules:
            try:
                module = Module.objects.get(id=mid)
                total_functional_days += module.functional_days or 0
                total_technical_days += module.technical_days or 0
            except Module.DoesNotExist:
                pass

        functional_cost = total_functional_days * 900
        technical_cost = total_technical_days * 800
        final_cost = functional_cost + technical_cost

        return JsonResponse({
            "success": True,
            "functional_days": total_functional_days,
            "technical_days": total_technical_days,
            "functional_cost": functional_cost,
            "technical_cost": technical_cost,
            "final_cost": final_cost
        })

    return JsonResponse({"success": False, "message": "Invalid request"})

def get_modules(request):
    product_id = request.GET.get('product_id')
    modules = []
    
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            # Assuming Product has a related_name 'modules' to access its modules
            modules = list(product.modules.values('id', 'name'))
        except Product.DoesNotExist:
            modules = []
    # If no product_id is provided, modules will be empty list by default
    
    return JsonResponse(modules, safe=False)

def get_submodules(request):
    module_id = request.GET.get("module_id")
    submodules = []

    if module_id:
        try:
            module = Module.objects.get(id=module_id)
            submodules = list(module.submodules.values("id", "name"))
        except Module.DoesNotExist:
            submodules = []

    return JsonResponse(submodules, safe=False)


def get_subsubmodules(request, submodule_id):
    subsubmodules = SubSubModule.objects.filter(submodule_id=submodule_id).values("id", "name")
    return JsonResponse(list(subsubmodules), safe=False)

def odoo_support(request):
    return render(request,'odoo_support.html')


def odoo_imple(request):
    return render(request,'odoo_imple.html')



def odoo_imple(request):
    return render(request,'odoo_imple.html')

def odoo_support(request):
    return render(request,'odoo_support.html')

def odoo_consulting(request):
    return render(request,'odoo_consulting.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Optional: Send Email
        try:
            send_mail(
                subject=f"New Contact Message from {name}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["neemkaroligroup@gmail.com"],  # Change with your email
                fail_silently=False,
            )
            messages.success(request, "Thank you for reaching out! We’ll get back to you soon.")
        except:
            messages.error(request, "Something went wrong while sending your message. Please try again.") # contact = name of url

    return render(request, "home.html")

def ai(request):
    return render(request,'AI.html')

def application(request):
    return render(request,'application.html')

def custom(request):
    return render(request,'custom.html')

def inte(request):
    return render(request,'inte.html')

def change(request):
    return render(request,'change.html')

def health(request):
    return render(request,'health.html')

def performance(request):
    return render(request,'performance.html')

def release(request):
    return render(request,'release.html')

def version(request):
    return render(request,'version.html')

def skill(request):
    return render(request,'skill.html')