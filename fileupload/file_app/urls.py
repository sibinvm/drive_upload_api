from django.urls import include, path
from .views import FileView

urlpatterns = [
    path('http://127.0.0.1:8000/file/upload/$', FileView.as_view(), name='file-upload'),
]