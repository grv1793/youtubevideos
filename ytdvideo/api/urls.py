from django.conf.urls import url

from api import views


urlpatterns = [
    url(r'^videos/$', views.VideoView.as_view(), name='get-videos'),
]
