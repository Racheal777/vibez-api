from datetime import timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like, Comment, HashTag, PostHashTag
from .serializers import PostSerializer, CommentSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import TokenAuthentication
import re

def extract_hashtags(content):
    hashtag = re.findall(r"#(\w+)", content)
    return hashtag



class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        post_data = request.data

        post_data['user'] = user.id

        serializer = PostSerializer(data=post_data, context={'request': request})

        if serializer.is_valid():

            post = serializer.save(user=request.user)
            content = post_data.get('content', '')
            hashtags = extract_hashtags(content)

            for tag_name in hashtags:
                hashtag, created = HashTag.objects.get_or_create(name=tag_name.lower())

                PostHashTag.objects.create(post=post, hashtag=hashtag, added_by=user )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostHashtagsView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, hashtag):
       try:
           hashtag_obj = HashTag.objects.get(name=hashtag)

           posts = Post.objects.filter(hashtags=hashtag_obj)

           serializer = PostSerializer(posts, many=True)
           return Response(serializer.data, status=status.HTTP_200_OK)

       except HashTag.DoesNotExist:
           return Response({"errors": "Hashtag not found"}, status=status.HTTP_404_NOT_FOUND)



class PostDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)


    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def update(self, request, pk):
        post = self.get_object(pk)
        if post.user != request.user:
            return  Response({"error": "You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)

        time_passed = timezone.now() - post.created_at

        if time_passed > timedelta(minutes=20):
            return Response({'error': 'You can only update posts within 20 minutes of creation'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            content = request.data.get('content', '')
            hashtags = extract_hashtags(content)

            post.hashtags.clear()

            for tag_name in hashtags:
                hashtag, created = HashTag.objects.get_or_create(name=tag_name.lower())

                PostHashTag.objects.create(post=post, hashtag=hashtag, added_by=request.user)
            serializer.save()

            return  Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        return  self.update(request, pk)


    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.user != request.user:
            return  Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class LikePostView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, post_id):
        user = request.user


        try:
            post = Post.objects.get(id=post_id)

        except Post.DoesNotExist:
            return Response({'error': "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=user, post=post)

        if not  created:
            like.delete()
            return Response({'message': "post unliked"}, status=status.HTTP_200_OK)
        return Response({'message': 'post liked'}, status=status.HTTP_201_CREATED)




class LikeCommentView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, comment_id):
        user = request.user

        try:
            comment = Comment.objects.get(id=comment_id)

        except Comment.DoesNotExist:
            return Response({'error': "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=user, comment=comment)

        if not  created:
            like.delete()
            return Response({'"message': "comment unliked"}, status=status.HTTP_200_OK)
        return Response({'message': 'comment liked'}, status=status.HTTP_201_CREATED)



class CommentPostView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, post_id= None, parent_id=None):
        user = request.user

        comment_data = request.data

        comment_data['user'] = user.id
        comment_data['post'] = post_id
        comment_data['parent'] = parent_id

        serializer = CommentSerializer(data=comment_data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class CommentDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)


    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        comment = self.get_object(pk)
        if comment.user != request.user:
            return  Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)