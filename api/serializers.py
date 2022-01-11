from django.conf import settings
from rest_framework import serializers
from posts.models import Question
from posts.models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('username',)

class QuestionSerializer(serializers.ModelSerializer):    
    user = serializers.StringRelatedField()
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', 'modified', 'user')
        read_only_fields = ('pub_date', 'modified', 'user') 

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    question = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = ('body', 'question', 'timestamp', 'user', 'modified')
        read_only_fields = ('question', 'timestamp', 'user', 'modified')

