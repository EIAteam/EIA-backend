from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectCreateSerializer,ProjectFileSerializer, ProjectUpdateSerializer, ProjectListSerializer,ProjectRetrieveSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Project,ProjectFile
from company.models import Company
from rest_framework.views import APIView
from django.conf import settings
from rest_framework import status

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

class ProjectFileViewset(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ProjectFile.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ProjectFileSerializer

    def get_queryset(self):
        if self.action=='list':
            return Project.objects.get(id=self.request.query_params['projectId']).projectFile.all()
        else:
            return ProjectFile.objects.all()

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=request.data['projectId'])
        my_file = request.FILES['file']
        projectFile=ProjectFile(project=project)
        projectFile.fileType=request.data['fileType']
        print(projectFile.fileType)
        print(projectFile.get_fileType_display())
        filePath=projectFile.uploadFilePath(my_file)
        projectFile.filePath=projectFile.filePath.storage.save(filePath,my_file)
        projectFile.name=projectFile.filePath.name.split('/')[-1]
        projectFile.save()
        return Response(status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.filePath.storage.delete(instance.filePath)
        instance.delete()





