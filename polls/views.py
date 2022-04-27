from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Room,Message,Topic
from django.contrib.auth.decorators import login_required #restricts a suer not logged in from carrying out ann cation
from django.contrib.auth.models import User 
from django.db.models import Q #django query model
from django.contrib.auth.forms import UserCreationForm# django inbuilt from for registering user
from django.http import HttpResponse
from .forms import RoomForm, InputMessage
from django.contrib.auth import authenticate,login,logout
# Create your views here.



#rooms=Room.objects.all
def room(request,pk):
    #pk(parameter key) is similar to an extension to the url originally typed in the views. 
    #eg, if the user types '...room/1/', the param key is 1
    #For this project, the pk is made to match the id of the rooms
    room=Room.objects.get(id=pk)
    messages=room.message_set.all().order_by('-created') # gets all the instances in model; Message that relates to the particular room
    participants=room.participants.all() # this is a many-many relationship
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('field')
        )
        room.participants.add(request.user)# adds a user that gives a request, i.e sends a message
        return redirect('room',pk=room.id)
    context={'room':room,'messages':messages,'participants':participants}
    form=InputMessage()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False) # saves
            room.host=request.user 
            room.save()
            context['form']=form
    return render( request, 'polls/room.html',context)


@login_required(login_url='login') #restricts/ rdirects the user to the login page at this point if not logged in
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()           
            return redirect('home')
    text={'form':form}
    return render(request, 'polls/room_form.html',text)


def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request. user !=  message.user or request.user.is_superuser:
        return HttpResponse("Tresspasser!!! Not Allowed")

    if request.method=='POST':
        key=message.room_id
        message.delete()
        return redirect('room',pk=key)
    return render(request,'polls/delete_message.html',{'obj':message})


@login_required(login_url='login')
def view_messages(request):
    user=User.objects.get(username=request.user.username)
    if request.user.is_superuser:
        messages=Message.objects.all
    else:
        messages=user.message_set.all().order_by('-created')
    context={'messages':messages,'page':'view'}
    return render(request, 'polls/message.html',context)


def home(request):
        #to make a database query
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
    Q(topic__name__icontains=q) | # will search the room by it's topic name. 'icontains automatically fills the search 
    Q(name__icontains=q) | #search the room by its own name
    Q(description__icontains=q) 
    ) 
    room_count=rooms.count() #accounts the number of rooms in the database
    topics=Topic.objects.all
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q)) #filters the messages displayed by the side
    room_messages=room_messages[:5]# i only want to get the most recent five objects of this to avoid the display running down the page
    context={'rooms':rooms, 'room_messages':room_messages,'topics':topics,'room_count':room_count}
    return render(request,'polls/home.html',context)


#def editMessage(request):
def user_profile(request,pk):
    user=User.objects.get(id=pk)
    room_messages=user.message_set.all()
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages,}
    return render(request,'polls/profile.html',context) 



@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user != room.host or request.user != User.user:
        return HttpResponse("Tresspasser!!! Not Allowed")
    text={'room':room}
    context={"form":form}
    return render(request, 'polls/room_form.html',context )


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User not registered')
            
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:  
            messages.error(request,'Username or Password not correct')
    context={'page':page}
    return render(request, 'polls/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid(): #confirms if the form is vaild
            user=form.save(commit=False)# setting this to false freezes sthe user details such that we can edit it
            user.username=user.username.lower()
            user.save() #saves the details of the user
            login(request,user)#logs the user in
            return redirect('home')
        else: messages.error(request, 'An error occured during registration')
    context={'form':form,"page":'register'}
    return render(request, 'polls/login_register.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'polls/.html',{'obj':room})
    
    #third parameter under the return is dict used for naming files in the html file
