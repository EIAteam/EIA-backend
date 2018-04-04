from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectCreateSerializer, ProjectUpdateSerializer, ProjectListSerializer,ProjectRetrieveSerializer,ProjectFileSereializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Project,BusinessLicenseFile,WorkshopEastImg,WorkshopLeaseContractFile,WorkshopNorthImg,WorkshopSouthImg,WorkshopWestImg,SiteUseFile,IdCardFile
from company.models import Company
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.parsers import MultiPartParser

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

class ProjectFileViewset(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ProjectFileSereializer


class ProjectFileView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def post(self, request,projectId,fileType,fileId):
        project=Project.objects.get(id=projectId)
        my_file = request.FILES['file']
        if fileType=='businessLicenseFile':
            businessLicense=BusinessLicenseFile(project=project)
            filePath = businessLicense.uploadFilePath(my_file)
            businessLicense.url=businessLicense.url.storage.save(filePath, my_file)
            businessLicense.name=businessLicense.url.name.split('/')[-1]
            businessLicense.save()
        elif fileType=="idCardFile":
            idCard = IdCardFile(project=project)
            filePath = settings.MEDIA_ROOT + '\\' + idCard.uploadFilePath(my_file)
            idCard.url = idCard.url.storage.save(filePath, my_file)
            idCard.name = idCard.url.name.split('/')[-1]
            idCard.save()
        elif fileType == "workshopLeaseContractFile":
            workshopLeaseContract = WorkshopLeaseContractFile(project=project)
            filePath = settings.MEDIA_ROOT + '\\' + workshopLeaseContract.uploadFilePath(my_file)
            workshopLeaseContract.url = workshopLeaseContract.url.storage.save(filePath, my_file)
            workshopLeaseContract.name = workshopLeaseContract.url.name.split('/')[-1]
            workshopLeaseContract.save()
        elif fileType == "siteUseFile":
            siteUseFile = SiteUseFile(project=project)
            filePath = settings.MEDIA_ROOT + '\\' + siteUseFile.uploadFilePath(my_file)
            siteUseFile.url = siteUseFile.url.storage.save(filePath, my_file)
            siteUseFile.name = siteUseFile.url.name.split('/')[-1]
            siteUseFile.save()
        elif fileType == "workshopEastImg":
            workshopEastImg = WorkshopEastImg(project=project)
            filePath = settings.MEDIA_ROOT + '\\' + workshopEastImg.uploadFilePath(my_file)
            workshopEastImg.url = workshopEastImg.url.storage.save(filePath, my_file)
            workshopEastImg.name = workshopEastImg.url.name.split('/')[-1]
            workshopEastImg.save()
        elif fileType == "workshopSouthImg":
            workshopSouthImg = WorkshopSouthImg(project=project)
            filePath = settings.MEDIA_ROOT + '\\' + workshopSouthImg.uploadFilePath(my_file)
            workshopSouthImg.url = workshopSouthImg.url.storage.save(filePath, my_file)
            workshopSouthImg.name = workshopSouthImg.url.name.split('/')[-1]
            workshopSouthImg.save()
        elif fileType == "workshopWestImg":
            workshopWestImg = WorkshopWestImg(project=project)
            filePath = settings.MEDIA_ROOT + '\\' + workshopWestImg.uploadFilePath(my_file)
            workshopWestImg.url = workshopWestImg.url.storage.save(filePath, my_file)
            workshopWestImg.name = workshopWestImg.url.name.split('/')[-1]
            workshopWestImg.save()
        elif fileType == "workshopNorthImg":
            workshopNorthImg = WorkshopNorthImg(project=project)
            filePath = settings.MEDIA_ROOT + '\\' + workshopNorthImg.uploadFilePath(my_file)
            workshopNorthImg.url = workshopNorthImg.url.storage.save(filePath, my_file)
            workshopNorthImg.name = workshopNorthImg.url.name.split('/')[-1]
            workshopNorthImg.save()
        else:
            return Response(status=404)
        return Response(status=204)

    def delete(self, request,projectId,fileType,fileId):
        if fileType=='businessLicenseFile':
            businessLicenseFile=BusinessLicenseFile.objects.get(id=fileId)
            businessLicenseFile.url.delete()
            businessLicenseFile.delete()
        elif fileType=="idCardFile":
            idCardFile=IdCardFile.objects.get(id=fileId)
            idCardFile.url.delete()
            idCardFile.delete()
        elif fileType == "workshopLeaseContractFile":
            workshopLeaseContractFile=WorkshopLeaseContractFile.objects.get(id=fileId)
            workshopLeaseContractFile.url.delete()
            workshopLeaseContractFile.delete()
        elif fileType == "siteUseFile":
            siteUseFile=SiteUseFile.objects.get(id=fileId)
            siteUseFile.url.delete()
            siteUseFile.delete()
        elif fileType == "workshopEastImg":
            workshopEastImg=WorkshopEastImg.objects.get(id=fileId)
            workshopEastImg.url.delete()
            workshopEastImg.delete()
        elif fileType == "workshopSouthImg":
            workshopSouthImg=WorkshopSouthImg.objects.get(id=fileId)
            workshopSouthImg.url.delete()
            workshopSouthImg.delete()
        elif fileType == "workshopWestImg":
            workshopWestImg=WorkshopWestImg.objects.get(id=fileId)
            workshopWestImg.url.delete()
            workshopWestImg.delete()
        elif fileType == "workshopNorthImg":
            workshopNorthImg=WorkshopNorthImg.objects.get(id=fileId)
            workshopNorthImg.url.delete()
            workshopNorthImg.delete()
        else:
            return Response(status=404)
        return Response(status=204)




