from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import UserRegisterSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import ConfirmationCode



@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(
    username=username,
    password=password,
    is_active=False
)
    
    code = str(random.randint(100000, 999999))
    ConfirmationCode.objects.create(
        user=user,
        code=code
    )

    return Response(data={'user_id': user.id,  "code": code}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def confirm_api_view(request):
    code = request.data.get('code')
    try:
        confirmation = ConfirmationCode.objects.get(code=code)
    except ConfirmationCode.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = confirmation.user
    user.is_active = True
    user.save()
    confirmation.delete()
    return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password) 
    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


