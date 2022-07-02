from django.shortcuts import render,HttpResponse
from api import views
from django.conf import settings
import requests
from video.models import Video
# Create your views here.

def fetch_videos(req):
    search_url='https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    
    search_params = {
            'part' : 'snippet',
            'q' : 'Cricket',
            'key' : settings.YOUTUBE_DATA_API_KEY,
             'maxResults' : 10,
             'type' : 'video'
        }
    video_ids=[]
    r=requests.get(search_url,params=search_params)
    print(r.json()['items'][0]['id']['videoId'])
    res=r.json()['items']
    for result in res:
         video_ids.append(result['id']['videoId'])

    video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 10
        }
    r = requests.get(video_url, params=video_params)
    results = r.json()['items']

    
    return HttpResponse(results)

# def index(req):
#     return render(req,'index.html')