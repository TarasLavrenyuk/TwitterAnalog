from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.welcome, name='welcome'),
    url(r'^login$', views.login, name='login'),
    url(r'^reg$', views.reg, name='reg'),
    url(r'^signup$', views.signUp, name='signup'),
    url(r'^saveChanges$', views.saveChanges, name='saveChanges'),
    url(r'^settings$', views.settings, name='settings'),
    url(r'^.{0,}$', views.name, name='name'),

)
