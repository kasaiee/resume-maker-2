"""
app_accoungin schema
"""
from django.contrib.auth import get_user_model
import graphene
from .types import UserType

User = get_user_model()

class Query(graphene.ObjectType):
    resume_maker_list = graphene.List(UserType)

    def resolve_resume_maker_list(root, info):
        return User.resume_makers.all()