#from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view #django UI for displaying an api
from chatapp.models import Room,Topic
from .serializers import serialRoom, serialTopic
@api_view(['GET'])
def getRoute(request):
    routes=[
        'GET/api/',
        'GET /api/rooms',
        'GET/ api/topics',
        'GET/api/rooms/:id',
    ]
    return Response(routes) #shows a documentation the api we've written
    #return JsonResponse(routes,safe=False)

@api_view(['GET','POST'])
def getRooms(request): # a view in the api to represent the rooms
    rooms=Room.objects.all()
    serializer =serialRoom(rooms,many=True)  #many=True because there are several fields
    return Response(serializer.data)


@api_view(['GET'],)
def getRoom(request,pk): # a view in the api to represent the rooms
    rooms=Room.objects.get(id=pk)
    serializer =serialRoom(rooms,many=False)  #many=True because there are several fields
    return Response(serializer.data)

@api_view(['GET'])
def getTopics(request):
    topics=Topic.objects.all()
    serializer = serial=serialTopic(topics,many=True)
    return Response(serializer.data)