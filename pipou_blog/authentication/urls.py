from django.urls import path
from .views import login_page, register_page
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_page, name='register'),
]
