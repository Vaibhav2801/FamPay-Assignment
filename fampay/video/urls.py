from rest_framework import routers
from django.urls import path, include
from video import views
router = routers.DefaultRouter()
router.register('', views.VideoViewSet)
from api import views

urlpatterns = [
    path('', include(router.urls)),
]
