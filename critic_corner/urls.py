"""critic_corner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from CriticCorner import views
from django.conf.urls.static import static
from critic_corner import settings
from django.conf import settings  # new
from django.urls import path, include  # new
from django.conf.urls.static import static  # new
from registration.backends.simple.views import RegistrationView 
from django.urls import reverse
from django.contrib.auth import views as auth_views

class MyRegistrationView(RegistrationView): 
    def get_success_url(self, user):
        return reverse('rango:register_profile')

urlpatterns = [
    path('', views.home, name='home'),
    path('CriticCorner/', include('CriticCorner.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='auth_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='auth_logout'),
    path('accounts/register/', RegistrationView.as_view(), name='registration_register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
