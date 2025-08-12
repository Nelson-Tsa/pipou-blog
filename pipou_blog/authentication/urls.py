from django.urls import path
from .views import CustomLoginView, register_page, debug_login, test_post, test_post_no_csrf
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_page, name='register'),
    path('debug-login/', debug_login, name='debug_login'),
    path('test-post/', test_post, name='test_post'),
    path('test-no-csrf/', test_post_no_csrf, name='test_no_csrf'),
]