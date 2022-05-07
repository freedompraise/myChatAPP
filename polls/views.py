from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Room,Message,Topic,User
from django.contrib.auth.decorators import login_required #restricts a suer not logged in from carrying out ann cation
#from django.contrib.auth.models import User 
from django.db.models import Q #django query model
#from django.contrib.auth.forms import UserCreationForm# django inbuilt from for registering user
from .forms import myUserForm
from django.http import HttpResponse
from .forms import RoomForm, UserForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.


@login_required(login_url='login')
def room(request,pk):
    #pk(parameter key) is similar to an extension to the url originally typed in the views. 
    #eg, if the user types '...room/1/', the param key is 1
    #For this project, the pk is made to match the id of the rooms
    room=Room.objects.get(id=pk)
    messages=room.message_set.all().order_by('-created') # gets all the instances in model; Message that relates to the particular room
    participants=room.participants.all # this is a many-many relationship
    if request.method=='POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('field')
        )
        room.participants.add(request.user)# adds a user that gives a request, i.e sends a message
        return redirect('room',pk=room.id)
    context={'room':room,'messages':messages,'participants':participants}
    return render( request, 'polls/room.html',context)



@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    topics=Topic.objects.all()    
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("Tresspasser!!! Not Allowed")
    
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    context={"form":form,'topics':topics,'room':room}
    return render(request, 'polls/room_form.html',context )


@login_required(login_url='login') #restricts/ rdirects the user to the login page at this point if not logged in
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name) #this creates a new topic if the input one is not in the database
        Room.objects.create(
            host= request.user,
            topic=topic,
            description=request.POST.get('description'),
            name=request.POST.get('name')
        )
        return redirect('home')
    text={'form':form,'topics':topics}
    return render(request, 'polls/room_form.html',text)


def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request. user !=  message.user or request.user.is_superuser==False:
        return HttpResponse("Tresspasser!!! Not Allowed")

    if request.method=='POST':
        key=message.room_id
        message.delete()
        return redirect('room',pk=key)
    return render(request,'polls/delete_message.html',{'obj':message})


def home(request):
        #to make a database query
    if request.method=='GET':
        q=request.GET.get('q') if request.GET.get('q')!=None else ''
        rooms=Room.objects.filter(
        Q(topic__name__icontains=q) | # will search the room by it's topic name. 'icontains automatically fills the search 
        Q(name__icontains=q) | #search the room by its own name
        Q(description__icontains=q) 
        ) 
        room_messages=Message.objects.filter(
            Q(room__name__icontains=q)|
            Q(body__icontains=q)|
            Q(room__topic__name=q)
            )
    room_count=rooms.count() #accounts the number of rooms in the database
    topics=Topic.objects.all()[:5]
     #filters the messages displayed by the side
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




def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'User not registered')
            
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:  
            messages.error(request,'Username or Password not correct')
    context={'page':page}
    return render(request, 'polls/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form=myUserForm()
    if request.method=='POST':
        form=myUserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
        else: messages.error(request,"Error Occured During Registration")
        return redirect('home')
    return render(request, 'polls/signup.html',{'form': form})
 

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'polls/delete.html',{'room':room})

@login_required(login_url='login')
def editUser(request):
    form=UserForm(instance=request.user)
    if request.method=='POST':
        form =UserForm(request.POST, request.FILES, instance=request.user,)
        form.save()
        return redirect('profile',pk=request.user.id)
    return render(request, 'polls/edit-user.html',{'form':form})
    #third parameter under the return is dict used for naming files in the html file

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request, 'polls/all_topics.html',{'topics':topics})

def activitiesPage(request):
    room_messages=Message.objects.all()
    return render(request,'polls/all_activities.html',{'messages':room_messages})