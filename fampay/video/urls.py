from rest_framework import routers
from django.urls import path, include
from video import views
router = routers.DefaultRouter()
router.register('', views.VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
