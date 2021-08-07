from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ratelimit.decorators import ratelimit
from rest_framework.authtoken.models import Token

# index
def home(request):
    return render(request, "index.html")

# dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    try:
        token = Token.objects.get(user=request.user).key
    except:
        token = "None"
    return render(request, "dashboard.html", {"title":"Something API - Dashboard", "token":f"{token}"})

# documentation
def documentation(request):
    return render(request, "documentation.html")

# registering user
from ratelimit.decorators import ratelimit
def register(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account was created succesfully.")
            return redirect("login")

    context = {"form": form}
    return render(request, "register.html", context)

# logging the user in
@ratelimit(key="ip", rate="5/m", method=["GET", "POST"], block=True)
def loginpage(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect credentials.")
            return render(request, "login.html")
    context = {}
    return render(request, "login.html", context)

# logging the user out
def logoutUser(request):
    logout(request)
    return redirect("index")