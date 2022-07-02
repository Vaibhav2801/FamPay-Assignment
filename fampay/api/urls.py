from django.urls import path, include
from api import views
urlpatterns = [
    path('', views.fetch_videos,name='fetch_videos'),
    path('video/', include('video.urls')),
]
