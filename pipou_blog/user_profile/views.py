from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserProfileForm
from authentication.models import User
from blog.models import Post

@login_required
def profile_view(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)

    user_posts = Post.objects.filter(user=user_profile)
    return render(request, 'user_profile/profile.html', {'user_profile': user_profile, "user_posts": user_posts})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'user_profile/edit_profile.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('login')
    return redirect('edit_profile')
