from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('list/<int:projectId>', views.list, name='diagramTextList'),
    path('create/', views.create, name='textCreate'),
    path('get/<int:diagramId>', views.get, name='diagramTextGet'),
    path('delete/<int:diagramId>', views.delete, name='diagramTextDelete'),
]
