from django.urls import path
from . import views
app_name='consulting_app'
urlpatterns = [
    path('',views.home_two ,name='home_two'),
    path('about/',views.about ,name='about'),
    path('vision/',views.vision ,name='vision'),
    path('leadership/',views.leadership ,name='leadership'),
    path('partnership/',views.partnership ,name='partnership'),
    path('blog/',views.blog ,name='blog'),
    path('blog/post/<int:post_id>/', views.blog_post, name='blog_post'),
    path("implementation/", views.implementation, name="implementation"),
    path("career/",views.career,name='career'),
    path("consulting/",views.cons,name='cons'),
    path("support/", views.support, name='support'),
    path('service/',views.micro_service,name='micro_service'),
]
