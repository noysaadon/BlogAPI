from rest_framework import serializers
from authenticate.serializers import UserSerializer
from blog.models import Blog, Like


class BlogSerializer(serializers.ModelSerializer):
    likeCounter = serializers.SerializerMethodField(method_name=None)
    class Meta:
        model = Blog
        fields = ('id','title','description', 'publisher', 'likeCounter')

    def get_likeCounter(self, obj):
        if Like.objects.filter(blog_id=obj.id).exists():
            likeCounter = Like.objects.filter(blog_id=obj.id).count()
            return likeCounter
        else:
            return 0

class BlogLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id','user', 'blog')