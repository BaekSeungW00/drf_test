from rest_framework import serializers
from .models import *
from users.models import User
from users.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    is_liked = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'
          
    def get_is_liked(self, obj):
        request= self.context.get('request')
        # if request.user.is_authenticated and PostLike.objects.filter(user=request.user, post=obj).exists():
        if PostLike.objects.filter(user=User.objects.get(id=1), post=obj).exists():
            return True
        else:
            return False
        
class PostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()
    
    class Meta:
        model = PostLike
        fields = '__all__'