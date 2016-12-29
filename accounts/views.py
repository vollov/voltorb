from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer

from app.permissions import IsAccountOwner
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

import logging
log = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
    #authentication_classes = (SessionAuthentication,)
    #permission_classes = (IsAuthenticated,IsAccountOwner)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    
from rest_framework.response import Response
from rest_framework.views import APIView


class ExampleView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        content = {
            'user': 'martin_test',  # `django.contrib.auth.User` instance.
            'auth': 'str_auth',  # None
        }
        return Response(content)

from django.contrib.auth import authenticate, login, logout
from rest_framework import status

class RegistrationView(APIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request, format=None):
        data = request.data
        
        username = data.get('username', None)
        password = data.get('password', None)
        log.debug('get login post with username = {0} and password = {1}'.format(username, password))
        
        account = authenticate(username=username, password=password)

        # fail, bad login info
        if account is None:
            return Response({
                'status': 'Unauthorized',
                'message': 'username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # fail, inactive account
        if not account.is_active:
            return Response({
                'status': 'Unauthorized',
                'message': 'This account has been disabled.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # success, login and respond
        login(request, account)
        serialized = UserSerializer(account)
        
        return Response(serialized.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)