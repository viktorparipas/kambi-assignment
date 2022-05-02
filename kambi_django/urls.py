"""kambi_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'files/', include('kambi_django.files_listing.urls')),
]

handler404 = 'kambi_django.files_listing.views.page_not_found_view'
handler500 = 'kambi_django.files_listing.views.error_view'
handler403 = 'kambi_django.files_listing.views.permission_denied_view'
handler400 = 'kambi_django.files_listing.views.bad_request_view'

