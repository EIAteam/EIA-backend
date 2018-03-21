from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project

# 获取自定义User
User = get_user_model()


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('projectName', 'company')


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'projectName', 'projectType', 'projectStatus', 'createTime', 'updateTime', 'agencyMessage',
                  'workerMessage', 'isMaterialEnough')
