from rest_framework import serializers
from .models import User
from posts.models import Post

class UserSerializer(serializers.ModelSerializer):
    post_num = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
    def get_post_num(self, obj):
        return Post.objects.filter(user=obj).count()
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)