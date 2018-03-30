from django.db import models
from django.contrib.auth import get_user_model
from company.models import Company

# 获取自定义User
User = get_user_model()


# Create your models here.


class Project(models.Model):
    """
    项目
    """
    PROJECTTYPE_CHOICES = (
        ('none', '无'),
        ('newBuilt', '新建'),
        ('extension', '扩建'),
        ('removal', '搬迁')
    )
    PROJECTSTATUS_CHOICES = (
        ('none', '无'),
        ('receivedInfo', '收到资料'),
        ('reportEdit', '报告编写'),
        ('InfoComplete', '资质材料完善'),
        ('submit', '入件'),
        ('investigate', '审批修改'),
        ('takeEvidence', '取证'),
    )
    ENERGYUSAGE_CHOICES = (
        ('NG','天然气'),
        ('LPG', '液化石油气'),
        ('none', '无')
    )
    agencyMessage = models.TextField(blank=True, null=True, verbose_name="中介留言")
    workerMessage = models.TextField(blank=True, null=True, verbose_name="编写员留言")
    isMaterialEnough = models.BooleanField(blank=True, default=False, verbose_name="中介材料齐全度")
    projectStatus = models.CharField(max_length=255, blank=True, choices=PROJECTSTATUS_CHOICES, default='none',
                                     null=True, verbose_name="项目状态")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_project")
    projectName = models.CharField(blank=True,max_length=255, unique=True, null=True, verbose_name="项目名称")
    createTime = models.DateField(auto_now_add=True, verbose_name="创建时间")
    updateTime = models.DateField(auto_now=True, verbose_name="更新时间")
    projectType = models.CharField(max_length=255, blank=True, choices=PROJECTTYPE_CHOICES, default='none', null=True,
                                   verbose_name="项目性质")
    constructionCompanyName = models.CharField(blank=True,max_length=255, null=True, verbose_name="建设单位名称")
    nameAbbreviation = models.CharField(blank=True,max_length=255, null=True, verbose_name="名称缩写")
    NEIType = models.CharField(blank=True,max_length=255, null=True,default='[]', verbose_name="国民经济行业类别及代码")
    environmentalEffectclassification = models.CharField(blank=True,max_length=255,default='[]',null=True, verbose_name="环境影响评价行业类别")
    EAcompanyName = models.CharField(blank=True,max_length=255, null=True, verbose_name="环评公司名称")
    EAcompanyCertificatenumber = models.CharField(blank=True,max_length=255, null=True, verbose_name="环评单位证书编号")
    EAcompanyTelephone = models.CharField(blank=True,max_length=255, null=True, verbose_name="环评单位联系电话")
    EAcompanyAddress = models.CharField(blank=True,max_length=255, null=True, verbose_name="环评单位联系地址")
    address = models.CharField(blank=True,max_length=255, null=True, verbose_name="项目地址")
    postalCode = models.CharField(blank=True,max_length=6, null=True, verbose_name="邮政编码")
    corporateName = models.CharField(blank=True,max_length=255, null=True, verbose_name="法人代表姓名")
    corporateId = models.CharField(blank=True,max_length=255, null=True, verbose_name="法人身份证")
    constructionScale = models.CharField(blank=True,max_length=50, null=True, verbose_name="项目规模")
    societyCreditcode = models.CharField(blank=True,max_length=20, null=True, verbose_name="统一社会信用代码")
    businessRange = models.CharField(blank=True,max_length=255, null=True, verbose_name="营业执照经营范围")
    contacts = models.CharField(blank=True,max_length=255, null=True, verbose_name="联系人")
    telephone = models.CharField(blank=True,max_length=255, null=True, verbose_name="联系电话")
    totalInvestment = models.FloatField(blank=True,null=True, verbose_name="项目总投资（万元）")
    environmentalProtectionInvestment = models.FloatField(blank=True,null=True, verbose_name="环保投资（万元）")
    floorSpace = models.FloatField(blank=True,null=True, verbose_name="占地面积（m2)")
    managementSpace = models.FloatField(blank=True,null=True, verbose_name="经营面积(m2)")
    nonAccommodationNum = models.IntegerField(blank=True,null=True, verbose_name="职工非住宿人数")
    accommodationNum = models.IntegerField(blank=True,null=True, verbose_name="职工住宿人数")
    dinningNum = models.IntegerField(blank=True,null=True, verbose_name="员工吃饭人数（人）")
    dayWorkTime = models.FloatField(blank=True,null=True, verbose_name="日工作时间")
    yearWorkTime = models.FloatField(blank=True,null=True, verbose_name="年工作时间")
    investmentTime = models.FloatField(blank=True, null=True, verbose_name="投产时间(年)")
    annualPowerConsumption = models.FloatField(null=True, verbose_name="电年耗量(万kwh/a)")
    annualLeftover = models.FloatField(null=True, verbose_name="边角料年产量")
    energyUse = models.CharField(max_length=255, null=True, verbose_name="能源使用情况")
    east = models.CharField(blank=True,max_length=255, null=True, verbose_name="东 ")
    south = models.CharField(blank=True,max_length=255, null=True, verbose_name="南")
    west = models.CharField(blank=True,max_length=255, null=True, verbose_name="西")
    north = models.CharField(blank=True,max_length=255, null=True, verbose_name="北")
    longtitude = models.FloatField(blank=True,null=True, verbose_name="经度")
    latitude = models.FloatField(blank=True,null=True, verbose_name="纬度")
    township = models.CharField(blank=True,max_length=255, null=True, verbose_name="所在区镇")
    specialOptionForSewageTreatmentWorks = models.CharField(blank=True,max_length=255, null=True, verbose_name="污水处理厂特别选项")
    pollutantHoldingWaterBody = models.CharField(blank=True,max_length=255, null=True, verbose_name="纳污水体")
    surfaceWaterQualityStandard = models.CharField(blank=True,max_length=255, null=True, verbose_name="地表水质量标准")
    surfaceWaterFunction = models.CharField(blank=True,max_length=255, null=True, verbose_name="地表水功能")
    soundEnvironmentStandard = models.CharField(blank=True,max_length=255, null=True, verbose_name="声环境质量标准")
    groundwaterArea = models.CharField(blank=True,max_length=255, null=True, verbose_name="地下水区域")
    groundwaterType = models.CharField(blank=True,max_length=255, null=True, verbose_name="地下水类型")
    groundwaterQualityStandard = models.CharField(blank=True,max_length=255, null=True, verbose_name="地下水质量标准")
    groundwaterBodyNumber = models.CharField(blank=True,max_length=255, null=True, verbose_name="地下水水体编号")
    besideWaterTreatmentPlant = models.CharField(blank=True,max_length=255, null=True, verbose_name="是否污水处理厂纳污范围")
    domesticSewageGo = models.CharField(blank=True,max_length=255, null=True, verbose_name="生活污水去向")
    domesticSewageEnvironmentImpactAnalysis = models.TextField(blank=True, null=True, verbose_name="生活污水环境影响分析")
    domesticSewageEmissionStandards = models.TextField(blank=True, null=True, verbose_name="生活污水排放标准")
    sensitivePointDistance = models.CharField(blank=True,max_length=255, null=True, verbose_name="敏感点距离")
    waterSourceDistance = models.CharField(blank=True,max_length=255, null=True, verbose_name="水源保护地距离")
    energyUsage = models.CharField(blank=True,max_length=255, null=True,choices=ENERGYUSAGE_CHOICES, verbose_name="能源使用情况")
    product = models.TextField(blank=True,null=True,default='[{}]',verbose_name="产品")
    material = models.TextField(blank=True,null=True,default='[{}]', verbose_name="材料")
    equipment = models.TextField(blank=True,null=True,default='[{}]', verbose_name="设备")
    exhaustGas = models.TextField(blank=True, null=True, default='[{}]', verbose_name="废气信息")
    emissionStandard = models.TextField(null=True,default='[{"standard":"","pollutant":"","pollutantOptions":[],"emissionMonitoring":"","maximumAllowableEmissionRate":"","maximumAllowableEmissionConcentration":""}]',verbose_name='废弃排放标准')
    environmentalEngineering = models.TextField(null=True,default='[{"project":"环保工程","content":"","use":""}]',verbose_name='环保工程')
    otherEngineering = models.TextField(null=True,default=
    '[{"project":"主体工程","content":"","use":""},{"project":"储运工程","content":"","use":""},{"project":"辅助工程","content":"","use":""},{"project":"公用工程","content":"","use":""}]',
                                            verbose_name='其他工程')
    sensitiveInfoWater = models.TextField(null=True,default=
    '[{"environmentalElements":"水环境","environmentalSensitivePoint":"","orientation":"","distance":"","environmentalObjective":""}]',
                                              verbose_name='水环境')
    sensitiveInfoAtmosphere = models.TextField(null=True,default=
    '[{"environmentalElements":"大气环境","orientation":"---","distance":"---","environmentalObjective":"《环境空气质量标准》（GB3095-2012）二级标准"}]',
                                                   verbose_name='大气环境')
    sensitiveInfoVoice = models.TextField(null=True,default=
    '[{"environmentalElements":"声环境","orientation":"---","distance":"---","environmentalObjective":""}]',
                                              verbose_name='声环境')
    sensitiveInfoReserve = models.TextField(null=True,default=
    '[{"environmentalElements":"","orientation":"","distance":"","environmentalObjective":""}]',
                                                verbose_name='居民区环境要素')
    sensitiveInfoHouse = models.TextField(null=True,default=
    '[{"environmentalElements":"","orientation":"","distance":"","environmentalObjective":""}]',
                                              verbose_name='水源保护区环境要素')


    """
    保留字段        
    """

    noiseEquipment = models.CharField(max_length=50, null=True, verbose_name="噪声污染源设备")
    noiseMonitoringPoints = models.IntegerField(null=True, verbose_name="噪声监测点数目")
    annualSolidWasteOutput = models.FloatField(null=True, verbose_name="包装袋年产量(t/a)")

    intermediarySourcesCompleted = models.CharField(max_length=5, blank=True, null=True, verbose_name="")
    intermediaryRemark = models.CharField(max_length=255, blank=True, null=True, verbose_name="")
    writerRemark = models.CharField(max_length=255, blank=True, null=True, verbose_name="")
    multi_project = models.IntegerField(blank=True, null=True, verbose_name="")

    def __str__(self):
        return self.projectName
