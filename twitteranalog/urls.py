from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.welcome, name='welcome'),
    url(r'^login$', views.sign_in, name='login'),
    url(r'^reg$', views.reg, name='reg'),
    url(r'^signup$', views.sign_up, name='signup'),
    url(r'^saveChanges$', views.save_changes, name='saveChanges'),
    url(r'^settings$', views.settings, name='settings'),
    url(r'^add_twit_view$', views.add_twit_view, name='add_twit_view'),
    url(r'^add_twit_action$', views.add_twit_action, name='add_twit_action'),
    url(r'^my_profile$', views.my_profile, name='profile'),
    url(r'^logout$', views.logout_action, name='logout'),
    url(r'^user_search$', views.user_search, name='user_search'),
    url(r'^twit_search$', views.twit_search, name='twit_search'),
    url(r'^unfollow$', views.unfollow, name='unfollow'),
    url(r'^follow$', views.follow, name='follow'),
    url(r'^followers=.{0,}', views.view_followers, name='view_followers'),
    url(r'^followings=.{0,}$', views.view_followings, name='view_followings'),
    url(r'^feed$', views.feed, name='feed'),
    url(r'^.{0,}$', views.profile, name='name'),

)
