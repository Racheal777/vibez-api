import os

from rest_framework import serializers
from .models import Post, Like, Comment, PostMedia, CommentMedia, HashTag
from ..uploads import upload_file


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['media_url', 'media_type', 'created_at']




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']



class CommentMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentMedia
        fields = ['media_url', 'media_type', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    media = CommentMediaSerializer(many=True, read_only=True)
    media_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'media_files', 'user', 'created_at','replies', 'post', 'parent', 'likes_count', 'media' ]
        read_only_fields = ['user', 'created_at']



    def get_replies(self, obj):

        replies = Comment.objects.filter(parent=obj).order_by('-created_at')
        return  CommentSerializer(replies, many=True).data



    def create(self, validated_data):

        media_data = validated_data.pop('media_files', [])

        comment = Comment.objects.create(**validated_data)

        for media_file in media_data:
            try:
                uploaded_media = upload_file(media_file)
                media_type = self.get_media_type(uploaded_media)

                CommentMedia.objects.create(
                    comment=comment,
                    media_url=uploaded_media,
                    media_type=media_type
                )
            except Exception as e:
                print(f"Error uploading media file: {media_file}. Error: {str(e)}")
        return comment

    def get_media_type(self, media_url):
        extension = os.path.splitext(media_url)[1].lower()
        print('eee', extension)

        if extension in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'image'
        elif extension in ['.mp4', '.mov', '.avi']:
            return 'video'
        else:
            return 'unknown'


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ['name']  # Add any additional fields as necessary


class PostSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments = serializers.SerializerMethodField()
    hashtags = HashTagSerializer(many=True, read_only=True)
    media_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )



    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj, parent=None).order_by('-created_at')
        return CommentSerializer(comments, many=True).data


    class Meta:
        model = Post
        fields = ['id', 'content', 'user', 'created_at','hashtags', 'comments', 'likes_count', 'media', 'media_files']
        read_only_fields = ['user', 'created_at']
        ordering = ['-created_at']


    def create(self, validated_data):
        media_data = validated_data.pop('media_files', [])
        post = Post.objects.create(**validated_data)

        for media_file in media_data:

            uploaded_media = upload_file(media_file)

            media_type = self.get_media_type(uploaded_media)

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

