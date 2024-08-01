from rest_framework import serializers
from django.contrib.auth import get_user_model
from app_accounting.models import Experience, Social

User = get_user_model()

class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()
    
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return 'http://localhost:8000' + obj.avatar.url if obj.avatar else ''
        # if obj.avatar:
        #     return 'http://localhost:8000' + obj.avatar.url
        # else:
        #     return ''

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "avatar", 'full_name']


class UserDetailSerializer(serializers.ModelSerializer):
    experiences = serializers.SerializerMethodField()

    def get_experiences(self, obj):
        experiences = obj.experiences.all()
        experiences_serielizer =  ExperienceSerializer(experiences, many=True).data
        return experiences_serielizer

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "avatar", "about", 'experiences']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "avatar", "about"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude  = ('user', )


class SocialSerializer(serializers.Serializer):
    url = serializers.URLField()

    def create(self, validated_data):
        """
        Create and return a new `Social` instance, given the validated data.
        """
        return Social.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Social` instance, given the validated data.
        """
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance