from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout #add this
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import loginform
import numpy as np
import pymongo
from datetime import datetime


client = pymongo.MongoClient('localhost', 27017)
db = client['farm']

# Create your views here.

def logot(request):
	logout(request)
	return redirect('/login/')

def home(request):
    return render(request,'feed_app/index.html')

def viewStock(request):
	collection1 = db['stock']
	stock = collection1.find_one({},{'_id':0})
	s={}
	for i in stock:
		s[i]=stock[i]
	return render(request,'feed_app/stock.html',{'stock':s})

def viewStockRecord(request):
	collection1 = db['stockrecord']
	stock = collection1.find({},{'_id':0})
	s={}
	l=[]
	for i in stock[0]:
		l.append(i)
	ind = 0
	for i in stock:
		s[ind] = {}
		for j in i:
			# print(j)
			# print(i)
			s[ind][j]=i[j]
		ind+=1
	# print(s,l)
	return render(request,'feed_app/stockRecord.html',{'head':l,'body':s})



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

@login_required
def feedProduction(request):
	if request.method == 'POST':
		print('heree')
		r = request.POST['dropdown']
		q = request.POST['quantity']
		print(r,q)
		collection1 = db['stock']
		stock = collection1.find_one({},{'_id':0})
		s={}
		for i in stock:
			s[i]=stock[i]
		# print(s)
		col = db['formula']
		frm = col.find_one({'type':r},{'_id':0,'ing':1})
		formula = {}
		for i in frm:
			formula = (frm[i])
		f = col.find({},{'_id':0})
		d ={}
		ind=0
		for i in f:
			d[ind] = i['ing']
			ind+=1
		lim = list(np.zeros(len(d[0])))
		# print(lim)
		for i in d:
			ind=0
			for j in d[i]:
				# print(d[i][j])
				if int(lim[ind])<int(d[i][j]):
					lim[ind] = d[i][j]
				ind+=1
		for i in range(len(lim)):
			lim[i]=lim[i]*7
		# for i in formula:
		# 	print(i,formula[i])
		# 	print(i,s[i])
		col1 = db['stockrecord']
		now = datetime.now()
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		col1.insert_one({'date time':dt_string,'qty':q,'feedType':r})
		for i in s:
			col1.update_one({'date time':dt_string},{"$set":{i:float(s[i])-float(int(q)*formula[i])}})
		for i in s:
			collection1.update_one({},{"$set":{i:float(s[i])-float(int(q)*formula[i])}})
		stock = collection1.find_one({},{'_id':0})
		l={}
		ind=0
		for i in stock:
			print(i,lim[ind])
			if float(stock[i])<float(lim[ind]):
				l[i]=stock[i]
			ind+=1
		print(l)
		return mpage(request,l)
		

	else:
		collection = db['formula']
		res = collection.find({},{'_id':0,'type':1})
		f=[]
		for i in res:
			for j in i:
				f.append(i[j])
		print(f)
		return render(request,'feed_app/feedProduced.html',{'feeds':f})


def mpage(request,msg={}):
	col = db['formula']
	f = col.find({},{'_id':0})
	d ={}
	ind=0
	for i in f:
		d[ind] = i['ing']
		ind+=1
	lim = list(np.zeros(len(d[0])))
	collection1 = db['stock']
	stock = collection1.find_one({},{'_id':0})
	l={}
	ind=0
	for i in stock:
		print(i,lim[ind])
		if float(stock[i])<float(lim[ind]):
			l[i]=stock[i]
		ind+=1
	print(l)
	return render(request,'feed_app/mpage.html',{'msg':l})

def apage(request):
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
		return render(request,'feed_app/apage.html',{'types':l})


def login(request):
	message=''
	if request.method == "POST":
		u = request.POST['uname']
		p = request.POST['pwd']
		# collection = db['login']
		# res = collection.find_one({'role':'man'})
		# uname = res['uname']
		# passw = res['password']
		user = authenticate(username=u,password=p)
		print(user)
		if user is not None:
			auth_login(request, user)
			message = f'Hello {user.username}! You have been logged in'
			print(message)
			if user.is_superuser:
				return redirect('/apage/')
			else:
				return redirect('/mpage/',{'msg':message})
		message = 'Login failed!'
	return render(request, "feed_app/mlogin.html",{'msg':message})


# def alogin(request):
# 	if request.method == "POST":
# 		u = request.POST['uname']
# 		p = request.POST['pwd']
# 		collection = db['login']
# 		res = collection.find_one({'role':'admin'})
# 		uname = res['uname']
# 		passw = res['password']
# 		if u==uname:
# 			if p==passw:
# 				+uname+'/')
# 	else:
# 		form = loginform()
# 		return render(request, "feed_app/alogin.html",{'form':form})




def newstock(request):
	if request.method == 'POST':
		print('heree')
		r = request.POST['dropdown']
		q = request.POST['quantity']
		print(r,q)
		collection = db['stock']
		stock = collection.find_one({},{'_id':0})
		
		v=0
		for i in stock:
			if i==r:
				v+=stock[i]
			
		v=int(v)
		q=int(q)
		collection.update_one({},{"$set": {r:v+q}})
		return mpage(request)






	else:
		collection = db['stock']
		res = collection.find({},{'_id':0})
		f=[]
		for i in res:
			for j in i:
				f.append(j)
		return render(request,'feed_app/newstock.html',{'ing':f})
