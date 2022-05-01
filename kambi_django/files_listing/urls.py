from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'files/(?P<folder_name>$)', views.list_files_view, name='files'),
    re_path(r'files/(?P<folder_name>[\w\d]+)', views.list_files_view, name='files'),
]
