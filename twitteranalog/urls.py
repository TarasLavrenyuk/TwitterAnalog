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
    url(r'^.{0,}$', views.profile, name='name'),

)
