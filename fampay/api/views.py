from django.shortcuts import render
from api import views
from django.conf import settings
import requests
# Create your views here.

def fetch_videos(req):
    search_url='https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    
    search_params = {
            'part' : 'snippet',
            'q' : 'learn Python',
            'key' : settings.YOUTUBE_DATA_API_KEY,
             'maxResults' : 10,
             'type' : 'video'
        }
    video_ids=[]
    r=requests.get(search_url,params=search_params)
   
    res=r.json()['items']
    for result in res:
        video_ids.append(result['id']['videp_Id'])

    return render(req,'api/index.html')

def index(req):
    return render(req,'index.html')