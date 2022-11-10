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

def update(request,type):
	if request.method == 'POST':
		for i in request.POST:
			if request.POST[i]!='' and i!='csrfmiddlewaretoken':
				collection = db['formula']
				# print(i)
				# {"$set"{:'{}.{}'.format(type,i):request.POST[i]}}
				collection.update_one({'type':type},{"$set":{'ing.{}'.format(i):request.POST[i]}})
		return HttpResponse('sucess')
	else:
		d={}
		collection = db['formula']
		res = collection.find_one({'type':type},{'_id':0,'ing':1})
		for j in res:
			d = (res[j])
		print(d)
		return render(request,'feed_app/update.html',{'data':d})


def mpage(request,uname):
	if request.method == 'POST':
		print('heree')
		r = request.POST['dropdown']
		q = request.POST['quantity']
		print(r,q)
		collection1 = db['stock']
		stock = collection1.find({},{'_id':0})
		s=[]
		for i in stock:
			for j in i:
				s.append(j)
		print(s)	
		return HttpResponse(r)
	else:
		collection = db['formula']
		res = collection.find({},{'_id':0})
		f=[]
		for i in res:
			for j in i:
				f.append(j)
		print(f)
		return render(request,'feed_app/mpage.html',{'user':uname,'feeds':f})

def apage(request,uname):
	if request.method == "POST":
		print('here')
		r = request.POST['dropdown']
		return redirect('/update/'+r+'/')
	else:
		collection = db['formula']
		res = collection.find({},{'_id':0,'type':1})
		l=[]
		for i in res:
			for j in i:
				l.append(i[j])
		# 	for j in i:
		# 		l.append(res)
		# print(l)
		# print(uname)
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