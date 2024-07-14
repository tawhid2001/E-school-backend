"""
URL configuration for e_school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
# from course import views
# from allauth.account.views import confirm_email
from accounts.views import UserUpdateView
from accounts.views import CustomConfirmEmailView,account_inactive

urlpatterns = [
    path('admin/', admin.site.urls),
    path('course/', include("course.urls")),
    path('department/', include("department.urls")),
    path('enroll/', include("enrollment.urls")),
    path('api-auth/', include("rest_framework.urls")),
    path('api/auth/user/update/', UserUpdateView.as_view(), name='rest_user_update'),
    path('api/auth/registration/', include("dj_rest_auth.registration.urls")),
    path('api/auth/', include("dj_rest_auth.urls")),
    path('api/auth/registration/account-confirm-email/<str:key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('account/inactive/', account_inactive, name="account_inactive"),
    path("api/auth/", include("django.contrib.auth.urls")),
]
