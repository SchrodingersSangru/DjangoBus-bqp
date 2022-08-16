"""djangobus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
# from django.conf.urls.static import staticsss
from user.views import RegisterView, UserProfileView, home, MyTokenObtainPairView, UserLogoutView, HelloView, ChangePasswordView

# import django.contrib.auth.views as auth_views
# from knox import views as knox_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
 
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'), 
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('home/', home, name='home'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('hello/', HelloView),
    path('changepassword/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('', include('user.urls')),
    path('buses/', include('bus.urls')),
]
