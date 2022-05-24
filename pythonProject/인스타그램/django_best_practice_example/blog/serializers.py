from rest_framework.serializers import ModelSerializer
from .models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        model = Post
        fields = ['id', 'message', 'created_at', 'user']
