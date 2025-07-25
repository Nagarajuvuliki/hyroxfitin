"""
URL configuration for hyroxin1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
def verify_otp_view(request):
    user_id = request.GET.get('user_id')
    return render(request, 'verify_otp.html', {'user_id': user_id})
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('hyroxinfit.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('accountcreate', TemplateView.as_view(template_name='createaccount.html'), name='account_createpate'),
    # path('hyrox/', include('hyrox.urls')),
    path('verify-otp/', verify_otp_view, name='verify_otp_page'),
    # path('', TemplateView.as_view(template_name='signin.html'), name='signin'),
    # # path('profile1', TemplateView.as_view(template_name='profile.html'), name='profile'),
    # path('pupdate', TemplateView.as_view(template_name='profileupdate.html'), name='pupdate'),
]