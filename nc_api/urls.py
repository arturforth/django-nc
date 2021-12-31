"""nc_api URL Configuration

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
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views   # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bills/', views.list_bills, name='list_bills'),
    path('api/bills/<int:pk>', views.detail_bill, name='detail_bill'),
    path('api/payments/', views.list_payments, name='list_payments'),
    path('api/payments/<int:id>', views.detail_payment, name='detail_payment'),
]

urlpatterns = format_suffix_patterns(urlpatterns)