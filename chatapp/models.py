from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField(unique=True)
    bio = models.TextField(null=True, blank = True)
    avatar = models.ImageField(null=True, blank = True)
    username = models.CharField(max_length=100, unique=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)# a many-to-many relationship
    updated=models.DateTimeField(auto_now=True) #will take a time stamp when the model is updated
    created=models.DateTimeField(auto_now_add=True) #auto_now_add only takes the first time. It does not update
    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['-updated','-created']

class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=[
            '-updated',
            '-created'
        ]
    def __str__(self):
        return self.body[0:30] 
