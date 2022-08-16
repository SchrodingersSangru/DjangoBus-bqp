from django.db import models

# Importing signals to implement auto action
from django.db.models.signals import post_save


from django.db import models


class user(models.Model):

     
    uid = models.UUIDField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company_name = models.CharField(max_length=30)
    is_user = models.BooleanField(default = True)
    is_manager = models.BooleanField(default = False)
    class Meta:
        db_table = "users"
        
  
    def __str__(self):
        return self.name



def post_user_created_signal(sender , instance , created , **kwargs):
    if created :
        if instance.is_manager:
            user.objects.create(user= instance)
    pass

post_save.connect(post_user_created_signal , sender= user)