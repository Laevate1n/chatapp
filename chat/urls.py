from django.urls import *
from .views import *

app_name='chat'

urlpatterns = [
    path('login',Login, name='login'),
    path('chatroom',ChatRoom, name='chatroom'),
    path('login/await/<int:status>',LoginAwait,name='await')
]
