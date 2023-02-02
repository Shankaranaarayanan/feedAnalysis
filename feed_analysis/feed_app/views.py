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
from feed_app.models import Stock,StockRecord,Formula
import json

# client = pymongo.MongoClient("mongodb+srv://farmManager:5obCKstgynDIfOAq@farmcluster.qlmwjkl.mongodb.net/?retryWrites=true&w=majority")
# db = client['farm']


# client = pymongo.MongoClient('localhost', 27017)
# db = client['farm']

# Create your views here.

def logot(request):
	logout(request)
	return redirect('/login/')

def home(request):
    return render(request,'feed_app/index.html')

def viewStock(request):
	# collection1 = db['stock']
	# stock = collection1.find_one({},{'_id':0})
	# s={}
	# for i in stock:
	# 	s[i]=stock[i]
	stock = Stock.objects.all()
	k = list(stock.values()[0].keys())
	s=(stock.values()[0])
	stock = {}
	for i in k:
		if i!='id':
			stock[i] = s[i]
	return render(request,'feed_app/stock.html',{'stock':stock})

def viewStockRecord(request):
	# collection1 = db['stockrecord']
	# stock = collection1.find({},{'_id':0})
	# s={}
	# l=[]
	# for i in stock[0]:
	# 	l.append(i)
	l = ['date time', 'qty', 'feedType', 'maize', 'jowar', 'Brice', 'DORB', 'SFPellet', 'DOGN', 'soya', 'RSM',
	'DDGS', 'GOC', 'calcitePowder', 'stoneGrid', 'DCP', 'methionine', 'lysine', 'aGeeMicForte', 'spectraDFM', 
	'synerzymeXL', 'choline', 'sodiumBicarbonate', 'salt', 'ultralyteC', 'sfCake']
	# ind = 0
	# for i in stock:
	# 	s[ind] = {}
	# 	for j in i:
	# 		# print(j)
	# 		# print(i)
	# 		s[ind][j]=i[j]
	# 	ind+=1
	# for i in s:
	# 	for j in range(len(l)):
	# 		try:
	# 			x=list(s[i].keys())[j]
	# 		except:print(s[i])
	# 		continue
	# 		print(s[i][x],l[j])
	stockrec = StockRecord.objects.all()
	k = list(stockrec.values()[0].keys())
	stock = {}
	for i in range(len(stockrec)):
		stock[i] = {}
		s=(stockrec.values()[i])
		# print(s)
		for j in k:
			if j!='id':
				stock[i][j]=s[j]
	return render(request,'feed_app/stockRecord.html',{'head':l,'body':stock})



def update(request,type):
	if request.method == 'POST':
		for i in request.POST:
			if request.POST[i]!='' and i!='csrfmiddlewaretoken':
				# print(i)
				# {"$set"{:'{}.{}'.format(type,i):request.POST[i]}}

				# collection = db['formula']
				# collection.update_one({'type':type},{"$set":{'ing.{}'.format(i):request.POST[i]}})
				obj, created = Formula.objects.update_or_create(
					type=type,
					defaults={i: request.POST[i]},
				)
		return HttpResponse('sucess')
	else:
		d={}
		# collection = db['formula']
		# res = collection.find_one({'type':type},{'_id':0,'ing':1})
		# for j in res:
		# 	d = (res[j])
		f = Formula.objects.filter(type = type).all()
		k = list(f.values()[0].keys())
		s = (f.values()[0])
		for i in k:
			if i!='id' and i!='type':
				d[i] = s[i]
		return render(request,'feed_app/update.html',{'data':d})

@login_required
def feedProduction(request):
	if request.method == 'POST':
		print('heree')
		r = request.POST['dropdown']
		q = request.POST['quantity']
		# print(r,q)
		# collection1 = db['stock']
		# stock = collection1.find_one({},{'_id':0})
		# s={}
		# for i in stock:
		# 	s[i]=stock[i]

		stock = Stock.objects.all()
		s={}
		k = list(stock.values()[0].keys())
		d = (stock.values()[0])
		for i in k:
			s[i] = d[i]
		# print(s)
		# col = db['formula']
		# frm = col.find_one({'type':r},{'_id':0,'ing':1})
		# formula = {}
		# for i in frm:
		# 	formula = (frm[i])

		formula = {}
		f = Formula.objects.filter(type = r).all()
		k = list(f.values()[0].keys())
		s = (f.values()[0])
		for i in k:
			if i!='id' and i!='type':
				formula[i] = s[i]

		# f = col.find({},{'_id':0})
		# d ={}
		# ind=0
		# for i in f:
		# 	d[ind] = i['ing']
		# 	ind+=1
		# lim = list(np.zeros(len(d[0])))
		# # print(lim)
		# for i in d:
		# 	ind=0
		# 	for j in d[i]:
		# 		# print(d[i][j])
		# 		if int(lim[ind])<int(d[i][j]):
		# 			lim[ind] = d[i][j]
		# 		ind+=1
		# for i in range(len(lim)):
		# 	lim[i]=int(lim[i])*7
		# # for i in formula:
		# # 	print(i,formula[i])
		# # 	print(i,s[i])
		# col1 = db['stockrecord']
		# now = datetime.now()
		# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		# col1.insert_one({'date time':dt_string,'qty':q,'feedType':r})
		# for i in s:
		# 	col1.update_one({'date time':dt_string},{"$set":{i:float(s[i])-float(int(q)*formula[i])}})
		# for i in s:
		# 	collection1.update_one({},{"$set":{i:float(s[i])-float(int(q)*int(formula[i]))}})
		# stock = collection1.find_one({},{'_id':0})
		# l={}
		# ind=0
		# for i in stock:
		# 	print(i,lim[ind])
		# 	if float(stock[i])<float(lim[ind]):
		# 		l[i]=stock[i]
		# 	ind+=1

		d = {}
		f = Formula.objects.all()
		k = list(f.values()[0].keys())
		s = f.values()
		lim = list(np.zeros(len(k)-2))
		# print(k)
		for i in s:
			ind = 0
			for j in i:
				# print(j)
				if j!='id' and j!='type':
					if int(lim[ind])<int(i[j]):
						lim[ind] = int(i[j])
					ind+=1
		for i in range(len(lim)):
			lim[i]=int(lim[i])*7
		now = datetime.now()
		dt_string = str(now)
		print(dt_string)
		# col1.insert_one({'date time':dt_string,'qty':q,'feedType':r})
		x = StockRecord(date_time=dt_string,qty=q,feed_type=r,**formula)
		x.save()
		f = Stock.objects.all()
		k = list(f.values()[0].keys())
		s = f.values()[0]
		ind = 0
		for i in formula:
			x = float(formula[i])
			formula[i] = float(s[i])-(x*float(q))
			ind+=1
		print(formula)
		Stock.objects.update(**formula)
		stock = Stock.objects.all()
		s = stock.values()[0]
		l={}
		ind=0
		for i in s:
			if i!='id':
				if float(s[i])<float(lim[ind]):
					l[i]=s[i]
				ind+=1
		return mpage(request,l)
		

	else:
		# collection = db['formula']
		# res = collection.find({},{'_id':0,'type':1})
		# f=[]
		# for i in res:
		# 	for j in i:
		# 		f.append(i[j])
		# print(f)

		frml = Formula.objects.all()
		fr = frml.values()
		f = []
		for i in fr:
			for j in i:
				if j=='type':
					f.append(i[j])
		return render(request,'feed_app/feedProduced.html',{'feeds':f})

@login_required
def mpage(request,msg={}):
	# col = db['formula']
	# f = col.find({},{'_id':0})
	# d ={}
	# ind=0
	# for i in f:
	# 	d[ind] = i['ing']
	# 	ind+=1
	# lim = list(np.zeros(len(d[0])))
	# collection1 = db['stock']
	# stock = collection1.find_one({},{'_id':0})
	# l={}
	# ind=0
	# for i in stock:
	# 	# print(i,lim[ind])
	# 	if float(stock[i])<float(lim[ind]):
	# 		l[i]=stock[i]
	# 	ind+=1
	# print(l)
	if msg=={}:
		f = Formula.objects.all()
		k = list(f.values()[0].keys())
		s = f.values()
		lim = list(np.zeros(len(k)-2))
		stock = Stock.objects.all()
		s = stock.values()[0]
		l={}
		ind=0
		for i in s:
			if i!='id':
				if float(s[i])<float(lim[ind]):
					l[i]=s[i]
				ind+=1
		msg = l
	return render(request,'feed_app/mpage.html',{'msg':msg})

def apage(request):
	if request.method == "POST":
		print('here')
		r = request.POST['dropdown']
		return redirect('/update/'+r+'/')
	else:
		# collection = db['formula']
		# res = collection.find({},{'_id':0,'type':1})
		# l=[]
		# for i in res:
		# 	for j in i:
		# 		l.append(i[j])
		frml = Formula.objects.all()
		fr = frml.values()
		l = []
		for i in fr:
			for j in i:
				if j=='type':
					l.append(i[j])
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
		# collection = db['stock']
		# stock = collection.find_one({},{'_id':0})
		# v=0
		# for i in stock:
		# 	if i==r:
		# 		v+=stock[i]
		# v=int(v)
		# q=int(q)
		# collection.update_one({},{"$set": {r:v+q}})
		stk = Stock.objects.all().values()[0]
		v=0
		s = {}
		for i in stk:
			if i==r:
				v+=int(stk[i])
			s[i]=stk[i]
		v+=int(q)
		s[r]=v
		Stock.objects.update(**s)
		return mpage(request)
	else:
		# collection = db['stock']
		# res = collection.find({},{'_id':0})
		# f=[]
		# for i in res:
		# 	for j in i:
		# 		f.append(j)

		stk = Stock.objects.all()
		st = stk.values()
		f = []
		for i in st:
			for j in i:
				if j!='id':
					f.append(j)
		return render(request,'feed_app/newstock.html',{'ing':f})
