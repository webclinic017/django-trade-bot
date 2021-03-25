from django.urls import path 

from accounts.api import UserList, user_detail, TeamList

urlpatterns = [
    path('', UserList.as_view()),
    path('<int:pk>', user_detail),
    
    path('teams/', TeamList.as_view())
]
