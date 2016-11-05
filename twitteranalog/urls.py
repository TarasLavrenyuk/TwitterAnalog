from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^login$', views.login, name='login'),
    url(r'^reg$', views.reg, name='reg'),
    url(r'^signup$', views.signup, name='signup'),

    ]
