from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('search/', views.youtube_search_view, name='youtube_search'),
    path('Search by year/', views.search_videos_by_year_view, name='Search_By_Year'),
]
