from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, null=True)
    hashtags = models.ManyToManyField("HashTag", related_name='posts', through='PostHashTag', )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class PostMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),


    ]

    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    media_url = models.URLField()
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for Post {self.post}"





class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes",  blank=True)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="likes",  blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post', 'comment')

    def __str__(self):
        return f"{self.user.username} liked a {self.post}"




class Comment(models.Model):
    content = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)

    def __str__(self):
        return self.content


class CommentMedia(models.Model):
        MEDIA_TYPES = [
            ('image', 'Image'),
            ('video', 'Video')
        ]

        comment = models.ForeignKey(Comment, related_name='media', on_delete=models.CASCADE)
        media_url = models.URLField()
        media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.media_type} for Comment {self.comment}"




class HashTag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)



class PostHashTag(models.Model):
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)
   date_added = models.DateTimeField(auto_now_add=True)
   added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

   class Meta:
       unique_together = ('post', 'hashtag')