from django.conf.urls import url
from home import views
from shopify_app.decorators import shop_login_required


urlpatterns = [
        url(r'^$', shop_login_required(views.MixedView.as_view()), name='root_path'),
        url(r'^design/$', views.design, name='root_design'),
        url(r'^export/$', views.export_csv, name='root_export'),
        url(r'^import/$', views.import_csv, name='root_import'),
        url(r'^mix/$', views.MixedView.as_view(), name='root_mix'),
        url(r'^welcome/$', views.welcome, name='root_welcome'),
]
