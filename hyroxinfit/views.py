from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm,ProfileForm
from .models import Profile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
@login_required
def home_view(request):

    return render(request, 'n_dashboard.html', {
        'username': request.user.username
    })
def testing_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # fname =request.POST['first_name']
            # lname=request.POST['last_name']
            # username=request.POST['last_name']
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('/login')  # Adjust as needed
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # fname =request.POST['first_name']
            # lname=request.POST['last_name']
            # username=request.POST['last_name']
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('/login')  # Adjust as needed
    else:
        form = RegisterForm()

    return render(request, 'n_register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Change 'home' to your homepage route
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'n_login.html', {'form': form})
@login_required
def profile_create(request):

    try:
        profile = request.user.profile
        is_update = True
    except Profile.DoesNotExist:
        profile = None
        is_update = False

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, user=request.user, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile saved successfully!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProfileForm(user=request.user, instance=profile)

    return render(request, 'n_profile.html', {
        'form': form,
        'profile_image': profile.profile_image if profile else None,
        'username': request.user.username,
        'is_update': is_update
    })
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/login')