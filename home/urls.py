from django.conf.urls import url
from home import views

urlpatterns = [
        url(r'^$', views.index, name='root_path'),
        url(r'^design/$', views.design, name='root_design'),
        url(r'^welcome/$', views.welcome, name='root_welcome'),
]
