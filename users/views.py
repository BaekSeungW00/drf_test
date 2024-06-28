from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import BasePermission, AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
# User FBV
@api_view(['GET', 'POST'])
def user_list_api_view(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    elif request.method == "POST":
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=HTTP_201_CREATED)
        return Response(user.errors, status=HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_retrieve_api_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
# User GenericAPIView
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        
class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'
    
# User ViewSet
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'
    """
    method: request method 지정(디폴트는 only GET), detail: url parameter 필요 여부(필수), 
    permission_classes: 퍼미션 클래스 지정(디폴트는 settings.py 참조),
    url_path: url 접미사(디폴트는 기본 url/함수명), url_name: url의 name 지정(디폴트는 소문자 모델명-함수명)
    """
    @action(methods=['POST'], detail=False, permission_classes=[AllowAny], 
            url_path='login', url_name='login') 
    def login_api_view(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.get(username=username)
        
        if not check_password(password, user.password):
            return Response(status=HTTP_401_UNAUTHORIZED)
        token = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response(
            status=HTTP_200_OK,
            data={
                'token': str(token.access_token),
                'user': serializer.data,
            }
        )
        
    @action(methods=['DELETE'], detail=True, permission_classes=[IsOwner],
            url_path='logout', url_name='logout')
    def logout_api_view(self, request, user_id):
        return Response(status=HTTP_204_NO_CONTENT)
        
@api_view(['POST'])
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.get(username=username)
    
    if not check_password(password, user.password):
        return Response(status=HTTP_401_UNAUTHORIZED)
    token = RefreshToken.for_user(user)
    serializer = UserSerializer(user)
    return Response(
        status=HTTP_200_OK,
        data={
            'token': str(token.access_token),
            'user': serializer.data,
        }
    )

@api_view(['DELETE'])
def logout_api_view(request):
    return Response(status=HTTP_204_NO_CONTENT)
        
@api_view(['GET'])
def check_auth(request):
    if request.user.is_authenticated:
        return Response(UserSerializer(request.user).data)
    return Response(status=HTTP_401_UNAUTHORIZED)



