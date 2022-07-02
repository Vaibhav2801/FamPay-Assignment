from django.shortcuts import render
from .serializers import VideoSerializer
from .models import Video
from video import views

# Create your views here.
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-upload_time')
    serializer_class = VideoSerializer
