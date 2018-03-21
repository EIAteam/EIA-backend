# Generated by Django 2.0.2 on 2018-03-21 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20180321_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='emissionStandard',
            field=models.TextField(default='[{}]', null=True, verbose_name='废弃排放标准'),
        ),
        migrations.AddField(
            model_name='project',
            name='environmentalEngineering',
            field=models.TextField(default="[{project:'环保工程',content:'',use:''}]", null=True, verbose_name='环保工程'),
        ),
        migrations.AddField(
            model_name='project',
            name='otherEngineeringData',
            field=models.TextField(default="[{'project':'主体工程','content':'','use':''},{'project':'储运工程','content':'','use':''},{'project':'辅助工程','content':'','use':''},{'project':'公用工程','content':'','use':''}]", null=True, verbose_name='环保工程'),
        ),
        migrations.AddField(
            model_name='project',
            name='sensitiveInfoAtmosphereData',
            field=models.TextField(default="{environmentalElements:'大气环境',orientation:'---',distance:'---',environmentalObjective:'《环境空气质量标准》（GB3095-2012）二级标准'}", null=True, verbose_name='大气环境'),
        ),
        migrations.AddField(
            model_name='project',
            name='sensitiveInfoHouseData',
            field=models.TextField(default="{environmentalElements:'',orientation:'',distance:'',environmentalObjective:''}", null=True, verbose_name='水源保护区环境要素'),
        ),
        migrations.AddField(
            model_name='project',
            name='sensitiveInfoReserveData',
            field=models.TextField(default="{environmentalElements:'',orientation:'',distance:'',environmentalObjective:''}", null=True, verbose_name='居民区环境要素'),
        ),
        migrations.AddField(
            model_name='project',
            name='sensitiveInfoVoiceData',
            field=models.TextField(default="{environmentalElements:'声环境',orientation:'---',distance:'---',environmentalObjective:''}", null=True, verbose_name='声环境'),
        ),
        migrations.AddField(
            model_name='project',
            name='sensitiveInfoWaterData',
            field=models.TextField(default="[{environmentalElements:'水环境',environmentalSensitivePoint:'',orientation:'',distance:'',environmentalObjective:''}]", null=True, verbose_name='水环境'),
        ),
    ]
