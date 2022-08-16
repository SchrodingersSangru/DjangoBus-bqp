# Importing base form class to create forms on the webpage
from django import forms
# Importing get_user_model to get auth user model
from django.contrib.auth import get_user_model
# Importing usercreationform to create user authentication model
from django.contrib.auth.forms import UserCreationForm , UsernameField
# Importing own created model
from .models import users


###########################################################################################################################
# Custom User Form for the Login of the Organisation 
###########################################################################################################################

# User = get_user_model()

        
        
class CreateModelForm(forms.ModelForm):
    class Meta:
        model = users
        fields = '__all__'