from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    telephone = models.CharField(max_length=15, null=True, verbose_name="手机")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username


class Company(models.Model):
    """
    公司
    """
    companyId = models.AutoField(primary_key=True)
    companyName = models.CharField(max_length=255, verbose_name="公司名称")


class CompanyUser(models.Model):
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
    userId = models.ForeignKey('User', on_delete=models.CASCADE)
    companyId = models.ForeignKey('Company', on_delete=models.CASCADE)
    position = models.CharField(max_length=15, choices=POSITION_CHOICES, default='worker', verbose_name="职位")


class Project(models.Model):
    """
    项目
    """
    projectId = models.AutoField(primary_key=True)  # 公司id primary_key
    workerId = models.ForeignKey('User', blank=True, null=True, related_name="workEnterprise",
                                 on_delete=models.DO_NOTHING)  # 对应
    agencyId = models.ForeignKey('User', blank=True, null=True, related_name="agencyEnterprise",
                                 on_delete=models.DO_NOTHING)  # 对应
    companyId = models.ForeignKey('Company', on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    NEIType = models.CharField(max_length=255, null=True, verbose_name="国民经济行业类别及代码")
    nameAbbreviation = models.CharField(max_length=255, null=True, verbose_name="名称缩写")
    enterpriseName = models.CharField(max_length=255, null=True, verbose_name="公司名称")
    companyName = models.CharField(max_length=255, null=True, verbose_name="环评公司名称")
    corporateId = models.CharField(max_length=18, null=True, verbose_name="法人身份证")
    corporateName = models.CharField(max_length=10, null=True, verbose_name="法人代表姓名")
    contacts = models.CharField(max_length=10, null=True, verbose_name="联系人")
    telephone = models.CharField(max_length=20, null=True, verbose_name="联系电话")
    postalCode = models.CharField(max_length=6, null=True, verbose_name="邮政编码")
    address = models.CharField(max_length=255, null=True, verbose_name="地址")
    totalInvestment = models.FloatField(null=True, verbose_name="项目总投资")
    environmentalProtectionInvestment = models.FloatField(null=True, verbose_name="环保投资")
    environmentalProtectionInvestmentProportion = models.FloatField(null=True, verbose_name="环保投资占比")
    energyUse = models.CharField(max_length=255, null=True, verbose_name="能源使用情况")
    floorSpace = models.FloatField(null=True, verbose_name="占地面积（m2)")
    managementSpace = models.FloatField(null=True, verbose_name="经营面积(m2)")
    nonAccommodationNum = models.IntegerField(null=True, verbose_name="职工非住宿人数")
    accommodationNum = models.IntegerField(null=True, verbose_name="职工住宿人数")
    dayWorkTime = models.FloatField(null=True, verbose_name="日工作时间")
    investmentTime = models.CharField(max_length=50, null=True, verbose_name="投资时间(年)")
    productNames = models.CharField(max_length=255, null=True, verbose_name="产品名称")
    constructionScale = models.CharField(max_length=50, null=True, verbose_name="建设规模")
    noiseEquipment = models.CharField(max_length=50, null=True, verbose_name="噪声污染源设备")
    noiseMonitoringPoints = models.IntegerField(null=True, verbose_name="噪声监测点数目")
    annualSolidWasteOutput = models.FloatField(null=True, verbose_name="包装袋年产量(t/a)")
    annualPowerConsumption = models.FloatField(null=True, verbose_name="年耗量(万kwh/a)")
    latitude = models.FloatField(null=True, verbose_name="纬度")
    longtitude = models.FloatField(null=True, verbose_name="经度")
    east = models.CharField(max_length=50, null=True, verbose_name="东 ")
    south = models.CharField(max_length=50, null=True, verbose_name="南")
    west = models.CharField(max_length=50, null=True, verbose_name="西")
    north = models.CharField(max_length=50, null=True, verbose_name="北")
    township = models.CharField(max_length=50, null=True, verbose_name="所在区镇")
    soundEnvironmentStandard = models.CharField(max_length=5, null=True, verbose_name="声环境质量标准")
    groundwaterArea = models.CharField(max_length=50, null=True, verbose_name="地下水区域")
    specialOptionforDaliang = models.CharField(max_length=5, null=True, verbose_name="大良特别选项")
    besideWaterTreatmentPlant = models.CharField(max_length=5, null=True, verbose_name="是否污水处理厂纳污范围")
    sensitivePointDistance = models.CharField(max_length=5, null=True, verbose_name="敏感点距离")
    waterSourceDistance = models.CharField(max_length=5, null=True, verbose_name="水源保护地距离")
    projectState = models.CharField(max_length=10, blank=True, null=True, verbose_name="")
    projectType = models.CharField(max_length=10, blank=True, null=True, verbose_name="项目类型")
    intermediarySourcesCompleted = models.CharField(max_length=5, blank=True, null=True, verbose_name="")
    intermediaryRemark = models.CharField(max_length=255, blank=True, null=True, verbose_name="")
    writerRemark = models.CharField(max_length=255, blank=True, null=True, verbose_name="")
    multi_project = models.IntegerField(blank=True, null=True, verbose_name="")

    def __str__(self):
        return self.enterpriseName


class Product(models.Model):
    """
    产品
    """
    productsId = models.AutoField(primary_key=True)  # 产品id primary_key
    enterpriseId = models.ForeignKey(Project, on_delete=models.CASCADE)  # 公司id foreign_key 多对一
    productsName = models.CharField(max_length=50, null=True, verbose_name="产品名称")
    num = models.BigIntegerField(null=True, verbose_name="数量")
    unit = models.CharField(max_length=20, null=True, verbose_name="单位")
    remark = models.CharField(max_length=50, null=True, verbose_name="备注")

    def __str__(self):
        return self.productsName


class Material(models.Model):
    """
    材料
    """
    materialId = models.AutoField(primary_key=True)
    enterpriseId = models.ForeignKey(Project, on_delete=models.CASCADE)
    materialName = models.CharField(max_length=50, verbose_name="材料名称")
    num = models.FloatField(null=True, verbose_name="数量")
    unit = models.CharField(max_length=20, null=True, verbose_name="单位")
    isOffcut = models.CharField(max_length=5, null=True, verbose_name="是否为边角料")
    state = models.CharField(max_length=10, null=True, verbose_name="状态")

    def __str__(self):
        return self.materialName


class Equipment(models.Model):
    """
    设备
    """
    equipId = models.AutoField(primary_key=True)
    enterpriseId = models.ForeignKey(Project, on_delete=models.CASCADE)
    equipmentName = models.CharField(max_length=50, verbose_name="设备名称")
    num = models.IntegerField(null=True, verbose_name="数量")
    unit = models.CharField(max_length=50, null=True, verbose_name="单位")
    remark = models.CharField(max_length=255, null=True, verbose_name="评论")

    def __str__(self):
        return self.equipmentName
