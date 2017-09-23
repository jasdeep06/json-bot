from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^chat_page/',views.chat_page,name='chat_page'),
    url(r'^accept_temp/',views.accept_temp,name='accept_temp')
]