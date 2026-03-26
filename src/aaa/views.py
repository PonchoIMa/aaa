from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import UserRegistrationSerializer, UserLoginSerializer
import datetime, jwt

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"}, 
                status = status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']

            payload = {
                'user_id' : user.id,
                'exp'     : datetime.datetime.utcnow() + datetime.timedelta(hours = 24), # Expires in 24h
                'iat'     : datetime.datetime.utcnow()
            }
            
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            
            return Response({
                "message": "Login successful",
                "token": token
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class DeactivateAccountView(APIView):
    def post(self, request):
        user = request.user 
        
        if(not user.is_authenticated):
            return Response({"error": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)
            
        user.is_active = False
        user.save()
        
        return Response({"message": "Account deactivated successfully"}, status = status.HTTP_200_OK)
