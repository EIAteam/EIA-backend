from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import CompanyListSerializer,CompanyCreateSerializer
from .models import Membership,Company

# 获取自定义User
User = get_user_model()


class CompanyListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CompanyListSerializer

    def get_queryset(self):
        return Membership.objects.filter(user=self.request.user)


class CompanyViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Company.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CompanyCreateSerializer



