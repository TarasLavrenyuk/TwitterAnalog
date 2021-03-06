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
    url(r'^twit_search.{0,}$', views.twit_search, name='twit_search'),
    url(r'^unfollow$', views.unfollow, name='unfollow'),
    url(r'^follow$', views.follow, name='follow'),
    url(r'^followers=.{0,}', views.view_followers, name='view_followers'),
    url(r'^followings=.{0,}$', views.view_followings, name='view_followings'),
    url(r'^feed$', views.feed, name='feed'),
    url(r'^like.{0,}$', views.like, name='like'),
    url(r'^statistics$', views.statistics, name='statistics'),
    url(r'^admin$', views.admin_page, name='suspicious_pages'),
    url(r'^see_blocked_users$', views.blocked_pages, name='blocked_pages'),
    url(r'^block$', views.block_user, name='block_user'),
    url(r'^unblock$', views.unblock_user, name='unblock_user'),
    url(r'^set_as_reliable$', views.set_as_reliable, name='set_as_reliable'),
    url(r'^report.{0,}$', views.report, name='report'),
    url(r'^.{0,}$', views.profile, name='name'),

)
