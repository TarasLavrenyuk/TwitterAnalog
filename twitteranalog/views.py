import re
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from models import Extra
from .db_class import Mongo
from .db_class import SQL

sql = SQL()
mongo = Mongo()


def welcome(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('./my_profile')
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


def my_profile(request):
    username = request.user.get_username()
    user_info = mongo.get_user_info(username)
    url = '/' + str(user_info['_id'])
    return HttpResponseRedirect(url)


@login_required(redirect_field_name='/')
def profile(request):
    # if request.user.is_superuser:
    #     print 'I am superuser!!!'
    # else:
    #     print 'I am not superuser!!!'

    current_username = request.user.get_username()
    line = request.path_info
    id = re.sub('[/]', '', line)
    # user_info = mongo.get_userinfo_by_twit_id(id)
    # if user_info:
    #     url = '/' + str(user_info['_id'])
    #     return HttpResponseRedirect(url)
    user_info = mongo.get_user_info_by_id(id)
    if user_info:
        twits = reversed(user_info['twits'])
        return render(request, 'profile.html',
                      {'user': user_info, 'twits': twits, 'current': current_username, 'return_url': request.path})
    user_info = mongo.get_user_info(id)
    if user_info:
        url = '/' + str(user_info['_id'])
        return HttpResponseRedirect(url)
    user_info = mongo.get_user_info(str(request.user))
    twits = reversed(user_info['twits'])
    return render(request, 'profile.html',
                  {'user': user_info, 'twits': twits, 'current': current_username, 'return_url': request.path})


def reg(request):  # view
    return render(request, 'reg.html', {'continents': sql.getContinents()})


def sign_up(request):  # action
    if sql.canSignUp(request) == False:
        return render(request, 'reg.html',
                      {'continents': sql.getContinents(), 'message': 'Such username is already exist'})
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
    return render(request, 'settings.html', {'user': mongo.get_user_info(request.user.get_username())})


def logout_action(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(redirect_field_name='/')
def add_twit_view(request):
    print request.user.get_group_permissions()
    return render(request, 'add_twit.html')


@login_required(redirect_field_name='/')
def add_twit_action(request):
    # print 'File:'
    # print request.FILES['my_file']
    hide = 0
    if request.POST.get('is_hide'):
        hide = 1
    username = request.user.get_username()
    mongo.add_twit(username, request.POST['header'], request.POST['content'], hide)
    return HttpResponseRedirect('./my_profile')


@login_required()
def user_search(request):
    name = request.GET['name']
    users = mongo.user_search(name)
    # print users[0]['hide']
    return render(request, 'users.html', {'users': users,
                                          'header': 'Search by "' + name + '"',
                                          'followings': mongo.get_user_followings_usernames(request.user.get_username())})


def twit_search(request):
    hashtag = request.REQUEST['hashtag']
    twits = mongo.twits_search(hashtag)
    header = 'Search by "' + hashtag + '"'
    followings = mongo.get_user_followings_usernames(request.user.get_username())
    return render(request, 'twits.html', {'twits': twits, 'header': header,
                                          'return_url': request.get_full_path(), 'followings': followings})


def unfollow(request):
    print request.GET['user']
    mongo.unfollow(request.user.get_username(), request.GET['user'])
    return HttpResponseRedirect(request.GET['user'])


def follow(request):
    print request.GET['user']
    mongo.follow(request.user.get_username(), request.GET['user'])
    return HttpResponseRedirect(request.GET['user'])


def view_followers(request):
    print request.path
    username = str(request.path).split("=", 1)[1]
    users = mongo.get_user_followers(username)
    return render(request, 'users.html', {'users': users,
                                          'header': '@' + username + ' followers',
                                          'followings': mongo.get_user_followings_usernames(request.user.get_username())})


def view_followings(request):
    print request.path
    username = str(request.path).split("=", 1)[1]
    users = mongo.get_user_followings(username)
    return render(request, 'users.html', {'users': users,
                                          'header': '@' + username + ' followings',
                                          'followings': mongo.get_user_followings_usernames(request.user.get_username())})


def feed(request):
    username = request.user.get_username()
    twits = mongo.feed(username)
    header = '@' + username + ' feed'
    followings = mongo.get_user_followings_usernames(request.user.get_username())
    return render(request, 'twits.html', {'twits': twits, 'header': header,
                                          'return_url': request.get_full_path(), 'followings': followings})


def like(request):
    print request.path
    # print request.REQUEST['return_url']
    twit_id = re.sub('/like=', '', request.path_info)
    print twit_id
    mongo.like(twit_id, request.user.get_username())
    return HttpResponseRedirect(request.GET['return_url'])


def statistics(request):
    online_users = get_online_users()
    last_week_twits = mongo.get_last_week_twits()
    last_month_twits = mongo.get_last_month_twits()
    most_popular_tags = mongo.get_popular_tags()
    most_popular_users = mongo.get_most_popular_users()
    most_active_users = mongo.get_most_active_users()
    # print most_popular_users['user']


    return render(request, 'statistics.html', {'online_users': online_users,
                                               'last_week_twits': last_week_twits,
                                               'last_month_twits': last_month_twits,
                                               'most_popular_tags': most_popular_tags,
                                               'most_active_users': most_active_users,
                                               'most_popular_users' : most_popular_users})


def get_online_users():
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=uid_list)