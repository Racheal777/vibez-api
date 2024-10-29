from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers  import UserSerializer
from django.contrib.auth import  authenticate
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token

class SignupView(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response({'user': UserSerializer(user).data,'token': token.key, 'message':'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        print(f'user {username}, pass {password}')
        if not username or not password:
            return Response({'errors': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            return Response({'user': UserSerializer(user).data,'token': token.key, 'message':'User retrieved successfully'}, status=status.HTTP_200_OK)
        return Response({'errors': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print(f'user {request.user.auth_token}')
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out'})
        except ObjectDoesNotExist:
            return Response({
                'errors': 'No active session found'
            }, status=status.HTTP_400_BAD_REQUEST)






