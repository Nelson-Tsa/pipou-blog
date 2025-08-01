from django.urls import path
from .views import CustomLoginView, register_page, debug_login, test_post
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_page, name='register'),
    path('debug-login/', debug_login, name='debug_login'),
    path('test-post/', test_post, name='test_post'),
]