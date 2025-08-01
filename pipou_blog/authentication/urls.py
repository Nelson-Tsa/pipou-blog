from django.urls import path
from .views import custom_login_view, register_page
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', custom_login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_page, name='register'),
]