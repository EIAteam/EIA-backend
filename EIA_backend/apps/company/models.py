from django.db import models
from django.contrib.auth import get_user_model

# 获取自定义User
User = get_user_model()


# Create your models here.


class Company(models.Model):
    """
    公司
    """
    users = models.ManyToManyField(User, through='Membership', related_name='companys')
    companyName = models.CharField(max_length=255, unique=True, null=True, verbose_name="公司名称")

    def __str__(self):
        return self.companyName


class Membership(models.Model):
    """
    公司职员职位表
    """
    POSITION_CHOICES = (
        ('supermanager', '超级管理者'),
        ('manager', '管理者'),
        ('worker', '编写员'),
        ('agency', '中介'),
        ('firstParty', '甲方'),
        ('noPosition', '无职'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userMembership')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='companyMembership')
    position = models.CharField(max_length=15, choices=POSITION_CHOICES, default='worker', verbose_name="职位")

    class Meta:
        unique_together = ("user", "company",)

    def __str__(self):
        return self.position
