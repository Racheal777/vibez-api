from gc import get_objects

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer
from rest_framework.generics import get_object_or_404



class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(request.data)

        post_data = request.data

        post_data['user'] = user.id

        print("Incoming data:", post_data)
        serializer = PostSerializer(data=post_data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PostDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.user != request.user:
            return  Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)