from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import dateparse
import urllib3
from django.http import HttpResponse

def call_api(request):
    if request.session.has_key('USERNAME'):
        username = request.session['USERNAME']
        accessCount = request.session['ACCESS_COUNT']
        accessTime = request.session['ACCESS_TIME']
        lastAccessTime = dateparse.parse_datetime(accessTime) #datetime.strptime(accessTime,'%H:%M:%S.%f')
        #  parser.isoparse(accessTime) #datetime.strptime(accessTime,'HH:MM:SS.mmmmmm')
        currentTime = datetime.now().time()
        timeDiff = datetime.combine(datetime.min, currentTime)  - datetime.combine(datetime.min, lastAccessTime.time())
        if timeDiff > timedelta(minutes=1):
            accessCount = 0
        accessCount+=1
        if(accessCount < 5):
             # apicall
             response = urllib3.PoolManager().request('GET','http://fastapi/items/5?q=somequery').data
             request.session['ACCESS_COUNT'] = accessCount
             request.session['ACCESS_TIME'] = datetime.now().isoformat()

             return HttpResponse(response, content_type='application/json')
             #n render(request,'result.html',{'result':response})
        return render(request,'access_denied.html')
    else:
        return redirect('login')
# Create your views here.
def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['USERNAME'] = user.username
            request.session['ACCESS_COUNT'] = 0
            request.session['ACCESS_TIME'] = datetime.now().isoformat()
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')


    else:
        return render(request,'login.html')

def register(request):

    if request.method == 'POST' :
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email exists')
                return redirect('register')
                
            else:    
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request,'User Created')
                return redirect('login')
        else:
            messages.info(request,'password didnt match')
            return redirect('register')
        
        return redirect('/')


    return render(request,'register.html')


def logout(request):
    auth.logout(request)
    clean_session(request)
    return redirect("/")

def clean_session(request):
    if request.session.has_key('USERNAME'):
        del request.session['USERNAME']
    if request.session.has_key('ACCESS_TIME'):
        del request.session['ACCESS_TIME']
    if request.session.has_key('ACCESS_COUNT'):
        del request.session['ACCESS_COUNT']