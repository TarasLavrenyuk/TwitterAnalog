from django.shortcuts import render
from django.http import HttpResponseRedirect
from .login import Login

lg = Login()

def welcome(request):
    return render(request, 'login.html')


def login(request):
    print 'I am here'
    print request.POST["username"]
    print request.POST["password"]

    result = lg.isLogin(request)
    if result == None:
        return HttpResponseRedirect('/')
    return render(request, 'profile.html', {'user_id' : result})



def reg(request):
    return render(request, 'reg.html')


def signup(request):
    result = lg.sugnup(request)
    return HttpResponseRedirect('/')