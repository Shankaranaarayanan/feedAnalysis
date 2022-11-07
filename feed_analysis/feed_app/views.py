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
	if request.method == 'POST':
		print('heree')
		r = request.GET['dropdown']
		print(r)
		return HttpResponse("sucess")
	else:
		return render(request,'feed_app/mpage.html',{'user':'Sorry you have enters the page without login'})

def apage(request,uname):
	if request.method == "POST":
		print('here')
		r = request.POST['dropdown']
		d={}
		collection = db['formula']
		res = collection.find({},{'_id':0})
		for i in range(res.count(True)):
			for j in res[i]:
				d[j]={}
				for k in res[i][j]:
					if i==r:
						d[j][k]=res[i][j][k]
		print(d)
		return HttpResponse("sucess")
	else:
		collection = db['formula']
		res = collection.find({},{'_id':0})
		l=[]
		for i in res:
			for j in i:
				l.append(j)
		print(uname)
		return render(request,'feed_app/apage.html',{'user':uname,'types':l})


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
					return redirect('/mpage/'+uname+'/')  
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
					return redirect('/apage/'+uname+'/')
	else:
		form = loginform()
		return render(request, "feed_app/alogin.html",{'form':form})