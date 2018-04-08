from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from .serializers import UserRegisterSerializer, UserDetailSerializer,UserUpdateSerializer
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# 获取自定义User
User = get_user_model()


class UserViewset(mixins.UpdateModelMixin,mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户注册与获取用户信息
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    # 登陆认证
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # 动态配置注册于获取信息的serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegisterSerializer
        elif self.action=='update' or self.action=='partial_update':
            return  UserUpdateSerializer
        return UserDetailSerializer

    # 动态配置注册与获取信息的permission（一个需要登陆，一个不需要）
    def get_permissions(self):
        if self.action == "retrieve" or self.action=='update' or self.action=='partial_update':
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    # 重载，如此retrieve与delete都是针对当前登陆的用户,/user/:id参数可以随意设定不影响
    def get_object(self):
        return self.request.user
