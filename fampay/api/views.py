from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
import requests
from video.models import Video
from rest_framework import pagination
from django.db.models import Q
import asyncio
from django.core.paginator import Paginator ,EmptyPage ,PageNotAnInteger
from asgiref.sync import sync_to_async
import time
# Create your views here.


# @sync_to_async
async def fetch_videos():
    
        search_url='https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
            
        search_params = {
                    'part' : 'snippet',
                    'q'  : 'cricket', 
                    'key' : settings.YOUTUBE_DATA_API_KEY,
                    'maxResults' : 10,
                    'type' : 'video'
                }
        video_ids=[]
        r=requests.get(search_url,params=search_params)
            
            # print(r.text)
        print(r.json()['items'][0]['id']['videoId'])
        
        
        
            #querying the videos with thier id
        res=r.json()['items']
        for result in res:
                video_ids.append(result['id']['videoId'])

        video_params = {
                    'key' : settings.YOUTUBE_DATA_API_KEY,
                    'part' : 'snippet,contentDetails',
                    'id' : ','.join(video_ids),
                    'maxResults' : 10
                }

                #querying detail infromation about the videos
        r = requests.get(video_url, params=video_params)
            # print(r.text)
        results =  r.json()['items']
        for result in results:
                    video_data = Video(
                        
                        video_id = result['id'],
                        title = result['snippet']['title'],
                        description = result['snippet']['description'],
                        url = f'https://www.youtube.com/watch?v={ result["id"] }',
                        upload_time = result['snippet']['publishedAt'],
                        thumbnail = result['snippet']['thumbnails']['high']['url']
                    )

                    print(video_data)
                    
                    video_data.save()
                    return redirect('home')    

# Creating Function which will fetch data from api and store it in databas
# Sending data to the index temmplate
def home(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main1(loop))
    loop.close()
    # f1 = loop.create_task(fetch_videos())
    # await asyncio.wait([f1])

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(fetch_videos())
    # loop.close()
    
#it will give a html response based on the query
    item = []
    item = Video.objects.all()
    if request.method == 'POST':
        if request.POST['submit'] == 'search':
            item = Video.objects.filter(
                Q(title__contains=request.POST['search'])      
            )
    
    p=Paginator(item,9)
    p_num=request.GET.get('page',1)
    print('Number of Pages')
    print(p.num_pages)
    try:
        page=p.page(p_num)
    except EmptyPage:
        page=p.page(1)
    context = {
    'videos' : page
    }
 
    return render(request, 'index.html', context)

# def index(req):
#     return render(req,'index.html')

async def function_asyc():
    
    for i in range(100000):
        if i % 50000 == 0:
            print("Hello, I'm Vaibhav")
              
            # New Line Added
            await asyncio.sleep(0.01)
    return 0

async def main1(loop):
    f1 = loop.create_task(fetch_videos())
    f2 = loop.create_task(function_asyc())
    await asyncio.wait([f1, f2])