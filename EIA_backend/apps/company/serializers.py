from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Company,Membership

# 获取自定义User
User = get_user_model()


class CompanyListSerializer(serializers.ModelSerializer):
    companyId=serializers.ReadOnlyField(source='company.id')
    companyName=serializers.ReadOnlyField(source='company.companyName')

    class Meta:
        model= Membership
        fields=('companyId','companyName','position')


class CompanyCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Company.objects.create(companyName=validated_data['companyName'])

    class Meta:
        model=Company
        fields=('id','companyName')


class MemberListSerializer(serializers.ModelSerializer):
    userId=serializers.ReadOnlyField(source='user.id')
    username=serializers.ReadOnlyField(source='user.username')
    email=serializers.ReadOnlyField(source='user.email')
    name=serializers.ReadOnlyField(source='user.name')
    class Meta:
        model= Membership
        fields=('userId','username','position','email','name')


class MembershipCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    companyName=serializers.CharField(source='company.companyName')

    def create(self, validated_data):
        user=User.objects.get(username=validated_data['user'])
        company=Company.objects.filter(companyName=validated_data['company']['companyName']).first()
        try:
            membership=Membership.objects.get(user=user,company=company,position='noPosition')
        except Membership.DoesNotExist:
            membership=Membership.objects.create(user=user,company=company,position='noPosition')
        return membership

    class Meta:
        model=Membership
        fields=('user','companyName')

class MembershipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Membership
        fields="__all__"














