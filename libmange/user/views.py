from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth import authenticate , login , logout
 
# Create your views here.

def signup_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        
        if password == confirm_password:
            user = User.objects.create_user(
                username = username,
                email = email ,
                password = password,
                phone = phone
            )    
            login (request , user)
            return HttpResponse('success')
        else:
            return HttpResponse ('passworrd Do Not Match')
    return render (request , 'user/signup.html')
    
    
def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username = username , password = password)
        
        if user is not None:
            login (request , user)
            return HttpResponse('OK')
        
        else: 
            return HttpResponse('Failed')
    return render(request , 'user/login.html')
    
    