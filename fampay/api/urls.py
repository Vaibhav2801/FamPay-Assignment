from django.urls import path
from api import views
urlpatterns = [
    path('', views.fetch_videos,name='fetch_videos'),
]
