from django.urls import path
from .views import csl , index


urlpatterns = [
    path('',index , name="index"),
    path('csl/',csl , name="csl")
]
