from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import user
# from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from knox.models import AuthToken
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
# JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('id', 'username', 'email')
        


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    company_name = serializers.CharField(write_only=True, required=True)
    is_superuser = serializers.BooleanField(default= False)
    
    class Meta:
        model = User
        #fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        fields = ['username', 'email', 'is_superuser', 'company_name', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': False},
            # 'is_superuser': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(

            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        
        user.save()

        return user
    

class ViewUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    first_name= serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    # password = serializers.CharField()
    is_superuser = serializers.CharField()
    class Meta:
        model = User 
        fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser')
        
        
    
    

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    permission_classes = (IsAuthenticated)
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['email'] = self.user.email 
        data['last name'] = self.user.last_name 
        # return data
        return data



### KEEP THIS CODE.. DON'T DELETE, IT'LL JUST GIVE BACK THE TOKENS, NOT OTHER INFO.. tHIS IS IMPORTANT TOO.. 
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['name'] = user.username
#         return token
    
    
class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def delete(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')



from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = user

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)