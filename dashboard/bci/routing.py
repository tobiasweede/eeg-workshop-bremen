from django.urls import path 
from .consumers import CslConsumer

ws_urlpatterns = [
    path("test1/",CslConsumer.as_asgi())
]