# Importing signals to implement auto action
from django.db.models.signals import post_save

import datetime
from django.db import models

class user(models.Model):
    
     
    uid = models.UUIDField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    SEX_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    
    age = models.IntegerField(default = 0)
    sex = models.CharField(choices=SEX_CHOICES, default='OTHER', max_length=100)
    email = models.EmailField(default = "", unique=True)
    address = models.CharField(max_length = 40, default= "")
    date_added = models.DateTimeField(default= datetime.datetime.now())

    # field to define user types
    is_manager = models.BooleanField(default =False)
    is_user = models.BooleanField(default= True)
    
    # class Meta:
    #     db_table = "users"
        
  
    def __str__(self):
        return self.name





def post_user_created_signal(sender , instance , created , **kwargs):
    if created :
        if instance.is_manager:
            user.objects.create(user= instance)
    pass

post_save.connect(post_user_created_signal , sender= user)
