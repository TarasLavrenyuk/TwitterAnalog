from django.shortcuts import render
from django.http import HttpResponseRedirect
from .db_class import SQL
from .db_class import Mongo
from .user import User

sql = SQL()
mongo = Mongo()
userId = 0


def welcome(request):
    return render(request, 'login.html')

def login(request):
    print request.POST["username"]
    print request.POST["password"]
    global userId
    userId = sql.isLogin(request)
    if userId == 0:
        return HttpResponseRedirect('/')
    user = mongo.getUserInfo(userId)
    if user == 0:
        mongo.addUser(userId)
    url = '/' + str(userId)
    return HttpResponseRedirect(url)

def profile(request):
    return render(request, 'profile.html', {'user_id' : id})

def reg(request):
    return render(request, 'reg.html', {'countries' : sql.getCountries()})

def signUp(request):
    if sql.canSignUp(request) == False:
        return render(request, 'reg.html', {'countries' : sql.getCountries(), 'message' : 'Such username is already exist'})
    sql.signUp(request)
    return HttpResponseRedirect('/')

def name(request):
    result = request.path
    return render(request, 'profile.html', {'user_id' : result})

def saveChanges(request):
    global userId
    mongo.updateProfile(request, userId)
    url = '/' + str(userId)
    return HttpResponseRedirect(url)

def settings(request):
    global userId
    print mongo.getUserInfo(userId)
    return render(request, 'settings.html', {'user' : mongo.getUserInfo(userId)})