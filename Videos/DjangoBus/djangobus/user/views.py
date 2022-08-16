from email.message import Message
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from django.shortcuts import render, redirect
from .models import user
from knox.models import AuthToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ViewUserSerializer
from .serializers import UserLogoutSerializer
from .serializers import ChangePasswordSerializer, MyTokenObtainPairSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView      ## this proves that we are using simple jwt for token authentication.. 
from django.contrib.auth.decorators import login_required, permission_required



class WelcomeView(APIView):
    
    def get(self, request):
        content = {'message': 'Welcome User'}
        return Response(content)



@login_required 
class HelloView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        content = {'message': 'Hello, ' + request.user.username}
        return Response(content)

##this serializer used to fetch username of the current user who is logged in.. 


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    



class RegisterView(generics.CreateAPIView):
    queryset = user.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {
            "success": True,
            "user": ViewUserSerializer(user, context=self.get_serializer_context()).data,
            "status code": status.HTTP_200_OK,
            "message": "User registered successfully",
            "token": AuthToken.objects.create(user)[1]
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)
        # return redirect('/login/')


## to make this run, provide bearer token in postman. 
class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ViewUserSerializer
    
    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
        #this is for redirecting to other view 
        # return redirect('/profile/', serializer.data)
        
       
        

##we have to pass Access_token in authentication, and refresh_token in body to make this working. 
class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete()

        return Response('user logged out successfully')

    

    



##just have to provide correct email as set with registration. 
## Password change works.. 
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = user
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return redirect('/profile/')
        
        
        
@api_view(['GET'])
def home(request):
    return Response({'Message' : 'Welcome to roboqop'  })
    # return render(request, 'users/templates/users/home.html', context)


@api_view(['GET'])
def about(request):
    return Response({'Your About Page'})