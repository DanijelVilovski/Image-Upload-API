from rest_framework import authentication, permissions, status
from rest_framework import permissions 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from users.serializers import UserSerializer

User = get_user_model()

@method_decorator(csrf_protect, name='dispatch')
class UserRegistration(APIView):
    permission_classes = (permissions.AllowAny, )

    #all users info
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    #create user 
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User successfully created!", status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')    
class UserDeletion(APIView):

    # permission_classes = (permissions.AllowAny, )

    #delete user
    def delete(self, request, pk, format=None):
        user = User.objects.get(id=pk)
        user.delete()
        return Response("User successfully deleted!", status=status.HTTP_204_NO_CONTENT)

@method_decorator(csrf_protect, name='dispatch')
class UserLogin(APIView):

    permission_classes = (permissions.AllowAny, )

    #log in user
    def post(self, request, format=None):
        user_name = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=user_name).first()
        if user is None:
            return Response('User does not exists!', status = status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response('Password invalid!', status = status.HTTP_406_NOT_ACCEPTABLE)
        if user.is_active:
            return Response('User is already logged in!', status = status.HTTP_406_NOT_ACCEPTABLE)
        user.is_active = True
        return Response("User successfully logged in!", status=status.HTTP_200_OK)

class UserLoginByID(APIView):

    # permission_classes = (permissions.AllowAny, )

    #user info by id
    def get(self, request, pk, format=None):
        users = User.objects.get(id=pk)
        serializer = UserSerializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #update user 
    def put(self, request, pk, format=None):
        # print(request.user.username)
        # user = User.objects.get(id=pk)
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User info successfully updated!", status = status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #log out user
    def delete(self, request, pk, format=None):
        user = User.objects.get(id=pk)
        user.is_active = False
        user.save()
        return Response("User successfully logged out!", status = status.HTTP_204_NO_CONTENT)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response("CSRF cookie set!", status=status.HTTP_200_OK)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CheckAuthenticated(APIView):
    def get(self, request, format=None):
        isAuthenticated = User.is_staff

        if isAuthenticated:
            return Response("User is authenticated!", status=status.HTTP_200_OK)
        else:
            return Response("User is not authenticated!", status=status.HTTP_401_UNAUTHORIZED)
     
    
