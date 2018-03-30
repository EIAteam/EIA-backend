from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectCreateSerializer, ProjectUpdateSerializer, ProjectListSerializer,ProjectRetrieveSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Project
from company.models import Company

# 获取自定义User
User = get_user_model()


class ProjectViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = Project.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            companyId = self.request.query_params.get('companyId')
            company = Company.objects.filter(users=self.request.user, id=companyId).first()
            return company.company_project.all()
        else:
            return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action == 'create':
            return ProjectCreateSerializer
        elif self.action == 'update':
            return ProjectUpdateSerializer
        elif self.action == 'partial_update':
            return ProjectUpdateSerializer
        elif self.action == 'retrieve':
            return ProjectRetrieveSerializer


