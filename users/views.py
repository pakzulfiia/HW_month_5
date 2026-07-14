from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import UserRegisterSerializer, UserAuthSerializer, ConfirmationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import ConfirmationCode
from rest_framework.generics import CreateAPIView,GenericAPIView




class RegistrationAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
            is_active=False,
        )

        code = str(random.randint(100000, 999999))

        ConfirmationCode.objects.create(
            user=user,
            code=code,
        )

        return Response({"user_id": user.id,"code": code,},
            status=status.HTTP_201_CREATED)
    
# @api_view(['POST'])
# def registration_api_view(request):
#     serializer = UserRegisterSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = User.objects.create_user(
#     username=username,
#     password=password,
#     is_active=False
# )
    
#     code = str(random.randint(100000, 999999))
#     ConfirmationCode.objects.create(
#         user=user,
#         code=code
#     )

#     return Response(data={'user_id': user.id,  "code": code}, status=status.HTTP_201_CREATED)


class ConfirmAPIView(GenericAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        confirmation = serializer.confirmation
        user = confirmation.user

        user.is_active = True
        user.save()

        confirmation.delete()

        return Response(status=status.HTTP_200_OK)
    
# @api_view(['POST'])
# def confirm_api_view(request):
#     code = request.data.get('code')
#     try:
#         confirmation = ConfirmationCode.objects.get(code=code)
#     except ConfirmationCode.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     user = confirmation.user
#     user.is_active = True
#     user.save()
#     confirmation.delete()
#     return Response(status=status.HTTP_200_OK)



class AuthorizationAPIView(GenericAPIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data["username"],
                            password=serializer.validated_data["password"],)

        if user is None:
            return Response({"error": "Invalid username or password."},
                            status=status.HTTP_401_UNAUTHORIZED,)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"key": token.key})
    
# @api_view(['POST'])
# def authorization_api_view(request):
#     serializer = UserAuthSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
    
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(username=username, password=password) 
#     if user is not None:
#         try:
#             token = Token.objects.get(user=user)
#         except:
#             token = Token.objects.create(user=user)
#         return Response(data={'key': token.key})
#     return Response(status=status.HTTP_401_UNAUTHORIZED)

