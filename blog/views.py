from django.shortcuts import render
from rest_framework import generics, permissions, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blog.models import Blog, Like
from rest_framework import viewsets, status
from blog.serializers import BlogLikeSerializer, BlogSerializer
from rest_framework.permissions import AllowAny
from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your views here.
class BlogViewSet(mixins.CreateModelMixin, 
                mixins.RetrieveModelMixin, 
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    update_data_pk_field = 'id'

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try: 
            serializer.is_valid(raise_exception=True)
            blog = serializer.save()
            return Response({
                "blog": BlogSerializer(blog, context=self.get_serializer_context()).data,
                "message": "Blog Created Successfully.",
            })

        except:
            message = {'detail': 'Error existed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args,  **kwargs):
        instance = self.get_object()
        if str(instance.publisher_id) != str(request.data.get("publisher")).strip():
            message = {'detail': 'You can not update this blog!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            return super().update(request, *args, **kwargs)

        except:
            message = {'detail': 'Error existed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if str(instance.publisher_id) != str(self.request.user.id):
                message = {'detail': 'You can not delete this blog!'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
        except Http404:
            message = {'detail': 'No Data Found'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogLikeViewSet(
                    mixins.CreateModelMixin, 
                    viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = BlogLikeSerializer

    def create(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        userId = request.data.get("user")
        blogId = request.data.get("blog")
        if Blog.objects.filter(id=blogId).exists():
            publisher_id = Blog.objects.get(id=blogId).publisher_id
            if str(publisher_id) == str(userId):
                message = {'detail': 'this blog was posted by you. So you can not like.'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if Like.objects.filter(user_id=userId, blog_id=blogId).exists():
            like = Like.objects.get(user_id=userId, blog_id=blogId)
            like.delete()
            message = {'detail': 'unliked'}
            return Response(message, status=status.HTTP_200_OK)
        try: 
            serializer.is_valid(raise_exception=True)
            blogLike = serializer.save()
            return Response({
                "blog": BlogLikeSerializer(blogLike, context=self.get_serializer_context()).data,
                "message": "BlogLike Created Successfully.",
            })

        except:
            message = {'detail': 'Error existed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
