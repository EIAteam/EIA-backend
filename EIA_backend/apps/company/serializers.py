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
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        company=Company.objects.create(companyName=validated_data['companyName'])
        membership=Membership(user=serializers.serializer_field.context['request'].user,company=company,position='noPosition')
        membership.save()
        return company

    class Meta:
        model=Company
        fields=('user','id','companyName')









