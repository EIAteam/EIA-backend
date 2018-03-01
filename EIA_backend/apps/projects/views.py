from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# 获取自定义User
User = get_user_model()

#class CompanyViewset(mixins.ListModelMixin):
