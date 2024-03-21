from django.urls import path
from .views import (UserRegisterView, url_validator,
                    HomeView, logout_user)

urlpatterns = [
    path('', url_validator, name='url_validator'),
    path('url_validator', url_validator, name='url_validator'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', logout_user, name='category-list'),
    path('home/', HomeView.as_view(), name='home'),
]
