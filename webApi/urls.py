from django.contrib import admin
from django.urls import path, include
from .views import HomesDataScraperViewset
from rest_framework import routers

api_router = routers.DefaultRouter()
api_router.register(r"homes", HomesDataScraperViewset, basename="homes")

urlpatterns = [

]
urlpatterns += api_router.urls


