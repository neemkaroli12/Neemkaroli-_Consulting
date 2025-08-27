from django.urls import path
from . import views
app_name='consulting_app'
urlpatterns = [
    path('',views.home_two ,name='home_two'),
    path('about/',views.about ,name='about'),
    path('vision/',views.vision ,name='vision'),
]
