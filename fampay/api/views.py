from django.shortcuts import render,HttpResponse
from api import views
from django.conf import settings
from django.http import JsonResponse
import requests
from video.models import Video
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
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
    for result in results:
            video_data = Video(
                
                video_id = result['id'],
                title = result['snippet']['title'],
                description = result['snippet']['description'],
                url = f'https://www.youtube.com/watch?v={ result["id"] }',
                upload_time = result['snippet']['publishedAt'],
                thumbnail = result['snippet']['thumbnails']['high']['url']
            )
            
            video_data.save()
    
    


async def home(request):    
    asyncio.ensure_future(fetch_videos())
    item = []
    if request.method == 'POST':
        if request.POST['submit'] == 'lucky':
            item = Video.objects.all()
        else:
            item = Video.objects.filter(
                Q(title__contains=request.POST['search'])      
            )
    context = {
    'videos' : item
    }
    return render(request, 'api/index.html', context)




# def index(req):
#     return render(req,'index.html')