
from django.urls import path
from .views import PostListView, PostDetailsView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailsView.as_view(), name='post-detail'),

]