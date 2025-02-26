from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, logout, login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from bs4 import BeautifulSoup
from .forms import LoginForm, RegisterForm
from .models import CustomUser, Location

def map(request):
    
    if request.user.is_authenticated == False:
        return redirect(login)
    
    return render(request, 'map.html')

def login(request):
    """Log user in"""

    # Forget any user_id
    request.session.flush()

    User = get_user_model()

    # If user is logged in, redirect to map page
    if request.user.is_authenticated:
        return redirect("map")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        form = LoginForm(request.POST)

        # Check form validity
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            #Authenticate user
            User = authenticate(request, username=username, password=password)

            if User is not None:
                django_login(request, User)
                request.session["User_id"] = User.id # Remember which user is logged in

                return redirect("map")

            else:
                messages.error(request, "User does not exist")
        
        else:
            messages.error(request, "Invalid username or password")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        form = LoginForm()

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        # Ensure username was submitted
        form = RegisterForm(request.POST)

        User = get.user.model()

        if form.is_valid():
            Username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            password_confirm = form.cleaned_data["password_confirm"]

            #check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, 'register.html', {'form': form})
            
            #check if password is confirmed properly
            if password != password_confirm:
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html', {'form': form})    
                    
            #create new user
            hashed_password = make_password(password)

            User = User.objects.create(username=username, password=hashed_password)
            User.save()

            return redirect("login")

    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})