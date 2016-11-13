from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.welcome, name='welcome'),
    url(r'^login$', views.sign_in, name='login'),
    url(r'^reg$', views.reg, name='reg'),
    url(r'^signup$', views.sign_up, name='signup'),
    url(r'^saveChanges$', views.save_changes, name='saveChanges'),
    url(r'^settings$', views.settings, name='settings'),
    url(r'^.{0,}$', views.profile, name='name'),

)
