from django.conf.urls import url
from shopify_app import views

urlpatterns = [
        url(r'^$', views.login, name='shopify_app_login'),
        url(r'^authenticate/$', views.authenticate, name='shopify_app_authenticate'),
        url(r'^finalize/$', views.finalize, name='shopify_app_finalize'),
        url(r'^logout/$', views.logout, name='shopify_app_logout'),
]
