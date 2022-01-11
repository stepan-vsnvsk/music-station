from django.shortcuts import get_object_or_404, render
from rest_framework import generics, viewsets
from posts.models import Question, Post
from .serializers import QuestionSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)    
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
