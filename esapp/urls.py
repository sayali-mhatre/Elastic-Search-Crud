from django.urls import path
from esapp import views

urlpatterns = [
    path('insert', views.insert_fileinfo),
    path('show', views.view_files),
    path('update', views.update_fileinfo),
    path('delete/<str:doc_id>', views.delete_fileinfo),
]
