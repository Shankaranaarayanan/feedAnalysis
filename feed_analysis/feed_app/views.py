from bson import is_valid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import loginform
import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client['farm']

# Create your views here.

def home(request):
    return render(request,'feed_app/index.html')


def mpage(request):
    return render(request,'feed_app/mpage.html',{'user':'Sorry you have enters the page without login'})

def apage(request):
	if request.method == "POST":
		print('here')
		r = request.GET['form']
		print(r)
	return render(request,'feed_app/apage.html',{'user':'Sorry you have enters the page without login'})


def mlogin(request):
	if request.method == "POST":
		form = loginform(request.POST)
		if form.is_valid():
			collection = db['login']
			res = collection.find_one({'role':'man'})
			uname = res['uname']
			passw = res['password']
			if form.cleaned_data['uname']==uname:
				if form.cleaned_data['password']==passw:
					return render(request,'feed_app/mpage.html',{'user' : form.cleaned_data['uname']})
	else:
		form = loginform()
		return render(request, "feed_app/mlogin.html",{'form':form})


def alogin(request):
	if request.method == "POST":
		form = loginform(request.POST)
		if form.is_valid():
			collection = db['login']
			res = collection.find_one({'role':'admin'})
			uname = res['uname']
			passw = res['password']
			if form.cleaned_data['uname']==uname:
				if form.cleaned_data['password']==passw:
					collection = db['formula']
					d = {}
					res = collection.find({},{'_id':0})
					l=[]
					for i in res:
						for j in i:
							l.append(j)
					# for i in range(res.count(True)):
					# 	for j in res[i]:
					# 		d[j]={}
					# 		for k in res[i][j]:
					# 			d[j][k]=res[i][j][k]
					# print(d)
					return render(request,'feed_app/apage.html',{'user' : form.cleaned_data['uname'],'types':l})
	else:
		form = loginform()
		return render(request, "feed_app/alogin.html",{'form':form})