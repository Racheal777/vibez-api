
from django.urls import path
from .views import PostListView, PostDetailsView, LikePostView, LikeCommentView, CommentDetailsView, CommentPostView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailsView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),

    path('posts/comment/<int:comment_id>/like/', LikeCommentView.as_view(), name='like-comment'),
    path('posts/<int:post_id>/comment/', CommentPostView.as_view(), name='post-comment'),

    path('comment/<int:pk>/comment/', CommentDetailsView.as_view(), name='comment-detail'),

]