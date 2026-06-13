
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

def login_view(request):
    error_message = None
    
    if request.method == "POST":
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # Authenticate user against Django's built-in User database
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            auth_login(request, user)
            return redirect('resume.html')  # Redirect to your resume dashboard page after successful login
        else:
            error_message = "Invalid username or password."
            
    return render(request, 'login.html', {'error': error_message})
