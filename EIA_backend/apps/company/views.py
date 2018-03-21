from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import CompanyListSerializer,CompanyCreateSerializer,MemberListSerializer,MembershipUpdateSerializer,MembershipCreateSerializer
from .models import Membership,Company
from rest_framework import status
from rest_framework.response import Response

# 获取自定义User
User = get_user_model()

class CompanyViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Company.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CompanyCreateSerializer

    def get_serializer_class(self):
        if self.action=='list':
            return CompanyListSerializer
        elif self.action=='create':
            return CompanyCreateSerializer

    def perform_create(self, serializer):
        company=serializer.save()
        membership = Membership(user=self.request.user, company=company,
                                position='superManager')
        return membership.save()


    def get_queryset(self):
        if self.action=='list':
            return Membership.objects.filter(user=self.request.user)
        elif self.action=='create':
            return Company.objects.all()






class MembershipViewSet(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = MemberListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return MemberListSerializer
        elif self.action == 'create':
            return  MembershipCreateSerializer
        elif self.action == 'update' or self.action=='partial_update':
            return MembershipUpdateSerializer

    def get_queryset(self):
        if self.action == 'list':
            companyId=self.request.query_params.get('companyId')
            company=Company.objects.filter(users=self.request.user,id=companyId).first()
            return company.companyMembership.all()
        elif self.action == 'create' or self.action == 'update' or self.action=='partial_update':
            return Membership.objects.all()

    def get_object(self):
        if self.action=='update' or self.action=='partial_update':
            companyId=self.request.data['company']
            userId=self.request.data['user']
            return Membership.objects.filter(company=companyId,user=userId).first()


    def create(self, request, *args, **kwargs):
        try:
            Company.objects.get(companyName=request.data['companyName'])
        except Company.DoesNotExist:
            return Response({'error': '公司不存在'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)










