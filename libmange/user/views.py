from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User  # Your custom user model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Import the Author model if it exists
from .models import Author  # Adjust the import path if needed
from library.models import Book
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        # New: Get the user type from the form ('user' or 'author')
        user_type = request.POST.get('user_type', 'user')
        
        if password == confirm_password:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone
            )
            # If the user selected "author", create an associated Author profile.
            if user_type == 'author':
                # Create the Author profile with default permissions
                Author.objects.create(
                    user=user,
                    can_create_tags=True,
                    can_add_books=True
                )
            login(request, user)
            return render(request , 'user/login.html')
        else:
            return HttpResponse('Passwords do not match')
    return render(request, 'user/signup.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request , 'library/home.html')
        else:
            return HttpResponse('Login failed')
    return render(request, 'user/login.html')

@login_required
def profile_view(request):
    """
    Display the profile page for the logged-in user.
    The template will have access to the current user via `request.user`.
    """
    return render(request, 'user/profile.html')

@login_required
def logout_view(request):                        
    logout(request)
    books = Book.objects.all()
    return render(request ,'library/home.html',{'books': books})