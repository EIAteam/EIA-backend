from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project,IdCardFile,BusinessLicenseFile,SiteUseFile,WorkshopWestImg,WorkshopSouthImg,WorkshopNorthImg,WorkshopLeaseContractFile,WorkshopEastImg

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


class ProjectRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

class BusinessLicenseFileSerializer(serializers.ModelSerializer):
    fileType = serializers.ReadOnlyField(default='businessLicenseFile')
    class Meta:
        model=BusinessLicenseFile
        fields = ('id','name','url','fileType')

class IdCardFileFileSerializer(serializers.ModelSerializer):
    fileType = serializers.ReadOnlyField(default='idCardFileFile')
    class Meta:
        model=IdCardFile
        fields = ('id','name','url','fileType')

class SiteUseFileSerializer(serializers.ModelSerializer):
    fileType = serializers.ReadOnlyField(default='siteUseFile')
    class Meta:
        model=SiteUseFile
        fields = ('id','name','url','fileType')

class WorkshopLeaseContractFileSerializer(serializers.ModelSerializer):
    fileType = serializers.ReadOnlyField(default='workshopLeaseContractFile')
    class Meta:
        model=WorkshopLeaseContractFile
        fields = ('id','name','url','fileType')

class WorkshopWestImgSerializer(serializers.ModelSerializer):
    fileType = serializers.ReadOnlyField(default='workshopWestImg')
    class Meta:
        model=WorkshopWestImg
        fields = ('id','name','url','fileType')

class WorkshopSouthImgSerializer(serializers.ModelSerializer):
    fileType = serializers.ReadOnlyField(default='workshopSouthImg')
    class Meta:
        model=WorkshopSouthImg
        fields = ('id','name','url','fileType')

class WorkshopNorthImgSerializer(serializers.ModelSerializer):
    fileType = serializers.ReadOnlyField(default='workshopNorthImg')
    class Meta:
        model=WorkshopNorthImg
        fields = ('id','name','url','fileType')

class WorkshopEastImgSerializer(serializers.ModelSerializer):
    fileType = serializers.ReadOnlyField(default='workshopEastImg')
    class Meta:
        model=WorkshopEastImg
        fields = ('id','name','url','fileType')



class ProjectFileSereializer(serializers.ModelSerializer):
    idCardFile=IdCardFileFileSerializer(many=True)
    businessLicenseFile=BusinessLicenseFileSerializer(many=True)
    siteUseFile=SiteUseFileSerializer(many=True)
    workshopLeaseContractFile=WorkshopLeaseContractFileSerializer(many=True)
    workshopWestImg=WorkshopWestImgSerializer(many=True)
    workshopSouthImg=WorkshopSouthImgSerializer(many=True)
    workshopNorthImg=WorkshopNorthImgSerializer(many=True)
    workshopEastImg=WorkshopEastImgSerializer(many=True)
    class Meta:
        model=Project
        fields=('idCardFile','businessLicenseFile','siteUseFile',
                'workshopLeaseContractFile','workshopWestImg','workshopSouthImg','workshopNorthImg','workshopEastImg')




