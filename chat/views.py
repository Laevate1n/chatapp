from django.shortcuts import render
from hashlib import md5
from django.http import *
from django.template import loader
from django.urls import reverse
from .models import *
from .forms import *
import firebase_admin
from firebase_admin import firestore,credentials
from google.cloud.firestore_v1.base_query import FieldFilter
# Create your views here.

cred = credentials.Certificate("chat/static/cred.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def Login(request):
    template = loader.get_template('Login.html')
    if request.session.get('loggedIn',False): 
        del request.session['userID']
        request.session['loggedIn'] = False
    print(request.session.get('userID','Logged Out'))
    if request.method == "POST":   
        form = UserForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['username']
            password = form.cleaned_data['password']
            data = db.collection('users').document(userName).get()
            print(data.to_dict())
            if not data.to_dict(): 
                print('it does not exist')
                newUser = {
                    'Name': userName,
                    'Password': password,
                    'allowed': False
                }
                db.collection('users').document(newUser['Name']).set(newUser)
                return HttpResponseRedirect(reverse('chat:await',kwargs={'status': 1}))
            if not data.to_dict()['Password'] == password:
                return HttpResponseRedirect(reverse('chat:await',kwargs={'status':2}))
            if data.to_dict()['allowed'] == False: 
                return HttpResponseRedirect(reverse('chat:await',kwargs={'status': 1}))
            request.session["userID"] = data.id
            request.session["loggedIn"] = True
            print(data.id)
            return HttpResponseRedirect(reverse('chat:chatroom'))
    else: form = UserForm()
    return render(request,'Login.html',{"form":form})

def LoginAwait(request,status):
    if status == 1: statusMsg = 'Your request awaits approval'
    if status == 2: statusMsg = 'Wronk password'
    return render(request,'LoginUpdate.html',{'status': statusMsg})

def ChatRoom(request):
    userID = request.session.get("userID",'system')
    context = {
        'userID' :userID
    }
    return render(request,'Messages.html',context)
