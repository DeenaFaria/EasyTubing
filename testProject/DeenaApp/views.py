from django.shortcuts import render
from googleapiclient.discovery import build
import datetime

# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')

def get_channel_id_by_name(channel_name, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id',
        maxResults=1
    )
    response = request.execute()
    if 'items' in response:
        return response['items'][0]['id']['channelId']
    return None

def search_youtube_channel(channel_id, query):
    youtube = build('youtube', 'v3', developerKey='AIzaSyADoVNJ667IDyY0ac8Q7fX-PQ2mKdRTsb0')
    request = youtube.search().list(
        q=query,
        channelId=channel_id,
        type='video',
        part='id,snippet',
        maxResults=50,
        order='relevance'
    )
    response = request.execute()
    return response.get('items', [])


def youtube_search_view(request):
    api_key = 'AIzaSyADoVNJ667IDyY0ac8Q7fX-PQ2mKdRTsb0'  

    if 'channel_name' in request.GET and 'query' in request.GET:
        channel_name = request.GET['channel_name']
        query = request.GET['query']
        channel_id = get_channel_id_by_name(channel_name, api_key)
        
        if channel_id:
            results = search_youtube_channel(channel_id, query)
            return render(request, 'youtube_search.html', {'results': results, 'channel_name': channel_name, 'query': query})
    
    return render(request, 'youtube_search.html')


def search_videos_by_year_view(request):
    api_key = 'AIzaSyADoVNJ667IDyY0ac8Q7fX-PQ2mKdRTsb0'

    channel_id = request.GET.get('channel_id')
    year = request.GET.get('year')

    channel_id = get_channel_id_by_name(channel_id, api_key)

    videos = []

    if channel_id and year:
        videos = search_videos_by_year(channel_id, int(year), api_key)

    current_year = datetime.datetime.now().year

    return render(request, 'Search_By_Year.html', {'videos': videos, 'current_year': current_year,  'year': year})

def search_videos_by_year(channel_id, year, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Define the start and end of the specified year
    start_date = f'{year}-01-01T00:00:00Z'
    end_date = f'{year + 1}-01-01T00:00:00Z'
    
    request = youtube.search().list(
        channelId=channel_id,
        type='video',
        part='id,snippet',
        maxResults=50,
        publishedAfter=start_date,
        publishedBefore=end_date
    )
    response = request.execute()
    return response.get('items', [])

