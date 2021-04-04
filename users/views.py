from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from library.models import UserItem
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() :
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    all_items = UserItem.objects.filter(owned_by=request.user)
    unused_items = UserItem.objects.filter(owned_by=request.user, consumed=True)
    used_items = UserItem.objects.filter(owned_by=request.user, consumed=False)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'all_items': all_items,
        'unused_items': unused_items,
        'used_items': used_items
    }

    return render(request, 'users/profile.html', context)

def public_profile(request, user):
    user = User.objects.get(username=user)
    items = UserItem.objects.filter(owned_by=user)
    context = {
        'user':user,
        'items': items
    }
    return render(request, 'users/public_profile.html', context)