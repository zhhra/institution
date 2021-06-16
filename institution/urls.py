from django.urls import path,include
from .views import getapi

app_name= 'institution'
urlpatterns = [
    path('api/class/<int:pk>', getapi , name= 'classroom'),
]