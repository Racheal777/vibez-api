import os

from rest_framework import serializers
from .models import Post, Like, Comment, PostMedia
from ..uploads import upload_file


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['media_url', 'media_type', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, read_only=True)
    media_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'content', 'user', 'created_at', 'media', 'media_files']
        read_only_fields = ['user', 'created_at']


    def create(self, validated_data):
        media_data = validated_data.pop('media_files', [])
        post = Post.objects.create(**validated_data)

        for media_file in media_data:

            uploaded_media = upload_file(media_file)
            print('ffff', uploaded_media)
            media_type = self.get_media_type(uploaded_media)

            print('yygby', media_type)
            PostMedia.objects.create(
                post=post,
                media_url=uploaded_media,
                media_type=media_type
            )

        return post



    def get_media_type(self, media_url):
        extension = os.path.splitext(media_url)[1].lower()
        print('eee', extension)

        if extension in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'image'
        elif extension in ['.mp4', '.mov', '.avi']:
            return 'video'
        else:
            return 'unknown'



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Post
        fields = ['id', 'content', 'image_url', 'user', 'file_url', 'video_url', 'created_at']
