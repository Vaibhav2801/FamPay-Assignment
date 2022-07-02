from django.shortcuts import render
from .serializers import VideoSerializer
from .models import Video
from video import views
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.
#querying all the video from the databse 
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-upload_time')
    serializer_class = VideoSerializer
    pagination_class=LimitOffsetPagination
