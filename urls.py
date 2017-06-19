from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^login/', include('shopify_app.urls')),
    url(r'^', include('home.urls'), name='root_path'),
    url(r'^admin/', admin.site.urls),
]
