from django.shortcuts import render

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.contrib.auth import logout


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        serializer = UserSerializerWithToken(self.user).data

        for key, value in serializer.items():
            if key == 'is_active' and value == False:
                return False
            data[key] = value
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register_user(request):
    data = request.data

    email = data['email']
    username = data["username"]
    password = data["password"]
    password2 = data['password2']

    if User.objects.filter(email=email).exists():
        return Response({"message": "User with this email already exists "}, status=status.HTTP_400_BAD_REQUEST)

    elif len(username) < 3:
        return Response({"message": "Username should contais at least 3 characters "}, status=status.HTTP_400_BAD_REQUEST)
    elif password != password2:
        return Response({
            "message": "Passwords do not match "
        }, status=status.HTTP_400_BAD_REQUEST)
    elif len(password) < 6:
        return Response({
            "message": "A strong password contains at least 6 characters "
        }, status=status.HTTP_400_BAD_REQUEST)

    else:
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    data = request.data

    email = data['email']
    username = data["username"]
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data["phone"]
    address = data["address"]
    avatar = request.FILES.get("avatar")
    print(f"hello guys this is avatar {avatar}")

    user.email = email
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.phone = phone
    user.address = address
    user.avatar = avatar

    user.save()

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def logout_request(request):
    user = request.user
    logout(request)
    return Response({"message": "logged out"})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    user = request.user
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request, id):
    user = User.objects.get(id=id)
    if user.is_staff:
        user.is_staff = False
    else:
        user.is_staff = True

    user.save()

    return Response({"message": "User role changed "})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()

    return Response({"message": "User Removed ", id: user.id})
