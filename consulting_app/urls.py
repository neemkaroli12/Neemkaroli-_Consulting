from django.urls import path
from . import views
app_name='consulting_app'
urlpatterns = [
    path('',views.home_two ,name='home_two'),
    path('about/',views.about ,name='about'),
    path('vision/',views.vision ,name='vision'),
    path('leadership/',views.leadership ,name='leadership'),
    path('blog/',views.blog ,name='blog'),
    path('blog/post/<int:post_id>/', views.blog_post, name='blog_post'),
    path("implementation/", views.implementation, name="implementation"),
    path("career/",views.career,name='career'),
    path("consulting/",views.cons,name='cons'),
    path("support/", views.support, name='support'),
    path('service/',views.micro_service,name='micro_service'),
    path('odoo-service/',views.odoo_service,name='odoo_service'),
    path('odoo_upgrade/',views.odoo_upgrade,name='odoo_upgrade'),
    path('estimate/', views.estimate_view, name='estimate'),
    path('get-modules/', views.get_modules, name='get_modules'),
    path('odoo_support/',views.odoo_support,name='odoo_support'),
]
