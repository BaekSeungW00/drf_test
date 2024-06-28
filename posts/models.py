from django.db import models
from users.models import User

class Post(models.Model):
    title = models.CharField(max_length=50, null=True)
    content = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_post')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_user')