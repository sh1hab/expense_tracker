from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

def register(request):
    """
    Handle user registration
    """
    if request.method == 'POST':
        # Use Django's built-in UserCreationForm
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            username = form.cleaned_data.get('username')
            form.save()
            
            # Add a success message
            messages.success(request, f'Account created for {username}! You can now log in.')
            
            # Redirect to login page
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    """
    User profile view
    """
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = Profile.objects.create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile
    }
    
    return render(request, 'profile.html', context)

def login(request):
    """
    Login view
    """


    form = UserCreationForm()


    return render(request, 'login.html', {'form': form})

def password_reset(request):
    """
    Password reset view
    """
    
    return render(request, 'password_reset.html')