from django.contrib import admin
from django.urls import  path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("pros/", views.pros, name='pros'),
    path('create/', views.create, name='textCreate'),
]
