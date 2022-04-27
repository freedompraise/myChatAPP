from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name="login"),
    path('',views.home,name='home'),
    path('register/',views.registerUser,name='register'),
    path('logout/',views.logoutUser,name='logout'),
    path('room/<str:pk>/',views.room, name='room'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('messages/',views.view_messages,name='messages'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
    #path('edit-message/<str:pk>/',views.editMessage,name='edit-message'),
    path('profile/<str:pk>/',views.user_profile,name='profile'),
]
