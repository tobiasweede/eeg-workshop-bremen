from django.shortcuts import render , HttpResponse
from django.shortcuts import  render, redirect
from .forms import UserLoginForm
from django.contrib.auth import login ,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this

# Create your views here.


def index(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})


def csl(request):
    return render(request,"csl.html",{})