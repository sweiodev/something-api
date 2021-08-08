from django.http.response import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ratelimit.decorators import ratelimit
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
import requests, os
from PIL import Image, ImageFilter
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from .usage import human_timedelta, uptime, usage
import datetime

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

    # gotta cache these things so it won't hurt my server, but it works for now. (update values once every x minutes)
    total = sum(usage.values())
    minutes_uptime = (datetime.datetime.utcnow() - uptime).total_seconds() / 60.0
    context = {
        "title":"Something API - Dashboard",
        "token":f"{token}",
        "uptime": human_timedelta(uptime),
        "triggered": usage['triggered'],
        "blur": usage['blur'],

        "total": total,
        "average": round(total/minutes_uptime, 1),
      }
    return render(request, "dashboard.html", context)

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



# API ----------------------------------
# image-manipulation
class Triggered(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            # creating the filename
            url = request.GET.get("avatar")
            filename = url.split("/")[4]

            # opening the avatar and the triggered and red pictures
            triggered = Image.open("api/utilities/triggered.png")
            red = Image.open("api/utilities/red.jpg")
            avatar = Image.open(requests.get(url, stream=True).raw)

            # pasting one on the other and saving and then sending the response, we also add the red blending
            avatar.paste(triggered, (0, 181))
            avatar = Image.blend(avatar.convert("RGBA"), red.convert("RGBA"), alpha=.4)
            avatar.save(f'files/{filename}_triggered.png', quality=95)
            file = open(f'files/{filename}_triggered.png', 'rb')

            usage['triggered'] += 1
            return FileResponse(file)
        finally:
            # deleting the created file after sending it
            os.remove(f"files/{filename}_triggered.png")

    def post(self, request):
        # not allowing methods other than GET
        return JsonResponse({"detail":"Method \"POST\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class Blur(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            # creating the filename
            url = request.GET.get("avatar")
            filename = url.split("/")[4]

            # opening the avatar and the triggered and red pictures
            avatar = Image.open(requests.get(url, stream=True).raw)

            # pasting one on the other and saving and then sending the response, we also add the red blending
            avatar = avatar.filter(ImageFilter.GaussianBlur(2))
            avatar.save(f'files/{filename}_blur.png', quality=95)
            file = open(f'files/{filename}_blur.png', 'rb')

            usage['blur'] += 1
            return FileResponse(file)
        finally:
            # deleting the created file after sending it
            os.remove(f"files/{filename}_blur.png")

    def post(self, request):
        # not allowing methods other than GET
        return JsonResponse({"detail":"Method \"POST\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
