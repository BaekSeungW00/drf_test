from .models import *
from .serializers import *
from users.models import *

from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import api_view
from rest_framework import generics

@api_view(['GET', 'POST'])
def post_list_api_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def post_retrieve_api_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data, status=HTTP_200_OK)
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(request.user)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        
@api_view(['POST', 'DELETE'])
def post_like_api_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        if PostLike.objects.filter(user=request.user, post=post).exists():
            return Response({'error': '사용자와 게시물 간 좋아요가 이미 존재함. '}, status=HTTP_409_CONFLICT)
        
        post_like = PostLike.objects.create(user=request.user, post=post)
        post_like.save()
        serializer = PostLikeSerializer(post_like)
        return Response(serializer.data, status=HTTP_201_CREATED)
    
    elif request.method == "DELETE":
        if not PostLike.objects.filter(user=request.user, post=post).exists():
            return Response({'error': '사용자와 게시물 간 좋아요가 존재하지 않음. '}, status=HTTP_409_CONFLICT)
        
        post_like = PostLike.objects.get(user=request.user, post=post)
        post_like.delete()
        return Response(status=HTTP_404_NOT_FOUND)