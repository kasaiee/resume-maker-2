from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import Group
from .serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from .pagination import StandardResultsPagination
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()

class UserList(generics.ListAPIView):
    """
    User List API
    ==========

    ## GET

    run `this code`
    
    after 
    
    ```
    this code
    ```
    
    ## POST

    """

    queryset = User.resume_makers.all()
    serializer_class = UserListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name']
    filterset_fields = ['groups']
    ordering_fields = ['id',]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            resume_maker = serializer.save()
            group_resume_makers = Group.objects.filter(name='resume_makers').first()
            resume_maker.groups.add(group_resume_makers)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class UserDetail(APIView):
    def get(self, request, user_id):
        user = User.resume_makers.filter(id=user_id).first()
        user_serializer = UserDetailSerializer(user)
        return Response(user_serializer.data)
    