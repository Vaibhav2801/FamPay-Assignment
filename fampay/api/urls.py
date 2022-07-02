from django.urls import path, include
from api import views
urlpatterns = [
    path('', views.home,name='home'),
    path('video/', include('video.urls')),
]
