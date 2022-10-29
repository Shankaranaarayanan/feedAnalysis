from bson import is_valid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import loginform

# Create your views here.

def home(request):
    return render(request,'feed_app/index.html')


def mpage(request):
    return render(request,'feed_app/mpage.html',{'user':'Sorry you have enters the page without login'})

def apage(request):
    return render(request,'feed_app/apage.html',{'user':'Sorry you have enters the page without login'})


def mlogin(request):
	if request.method == "POST":
		form = loginform(request.POST)
		if form.is_valid():
			if form.cleaned_data['uname']=='user1':
				if form.cleaned_data['password']=='user1':
					return render(request,'feed_app/mpage.html',{'user' : form.cleaned_data['uname']})
	else:
		form = loginform()
		return render(request, "feed_app/mlogin.html",{'form':form})


def alogin(request):
	if request.method == "POST":
		form = loginform(request.POST)
		if form.is_valid():
			if form.cleaned_data['uname']=='user1':
				if form.cleaned_data['password']=='user1':
					return render(request,'feed_app/apage.html',{'user' : form.cleaned_data['uname']})
	else:
		form = loginform()
		return render(request, "feed_app/alogin.html",{'form':form})