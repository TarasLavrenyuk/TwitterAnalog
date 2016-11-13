from django.shortcuts import render
from django.http import HttpResponseRedirect
from .db_class import SQL
from .db_class import Mongo
from django.contrib.auth.models import User
from models import Extra
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

sql = SQL()
mongo = Mongo()

def welcome(request):
    return render(request, 'login.html')

def sign_in(request):
    user = authenticate(username=request.POST["username"], password=request.POST["password"])
    if user is not None:
        login(request, user)
        username = user.get_username()
        user_info = mongo.get_user_info(username)
        url = '/' + str(user_info['_id'])
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/')

def profile(request):
    user_info = mongo.get_user_info(str(request.user))
    print user_info
    return render(request, 'profile.html', {'user' : user_info})

def reg(request): # view
    return render(request, 'reg.html', {'continents' : sql.getContinents()})

def sign_up(request): # action
    if sql.canSignUp(request) == False:
        return render(request, 'reg.html', {'continents' : sql.getContinents(), 'message' : 'Such username is already exist'})
    new_user = User.objects.create_user(request.POST["username"], 'email', request.POST["password"])
    Extra(continent=request.POST["continent"], user=new_user).save()
    mongo.add_user(new_user.get_username(), request.POST["continent"])
    return HttpResponseRedirect('/')

def save_changes(request):
    mongo.update_profile(request, request.user.get_username())
    user_info = mongo.get_user_info(request.user.get_username())
    url = '/' + str(user_info['_id'])
    return HttpResponseRedirect(url)

@login_required(redirect_field_name='/')
def settings(request):
    print request.user
    return render(request, 'settings.html', {'user' : mongo.get_user_info(request.user.get_username())})

@login_required(redirect_field_name='/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')