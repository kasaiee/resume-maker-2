from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from app_accounting.models import Experience

User = get_user_model()


class ExperienceType(DjangoObjectType):
    class Meta:
        model = Experience
        exclude = ('user', )


class UserType(DjangoObjectType):
    avatar = graphene.String()

    def resolve_avatar(root, info):
        return "http://localhost:8000" + root.avatar.url if root.avatar else ''
    
    # experience_list = graphene.List(ExperienceType)

    # def resolve_experience_list(root, info):
    #     return root.experiences.all()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "avatar", 'full_name', 'experiences')
