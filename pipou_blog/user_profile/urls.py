from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.profile_view, name='profile'),
    path('modifier/', views.edit_profile_view, name='edit_profile'),
    path('supprimer/', views.delete_account_view, name='delete_account'),
]