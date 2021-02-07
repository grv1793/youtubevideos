from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include

urlpatterns = [
    url(r'api/', include('api.urls')),
    url(r'^portal/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
