import xlwings as xw
import os
import pythoncom
import datetime
import random
import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Project
class Product:
    def __init__(self, productsName,num,unit,remark):
        self.productsName=productsName
        self.num=num
        self.unit=unit
        self.remark=remark

    def __str__(self):
        return self.productsName
class Equipment:
    def __init__(self,equipName,num,unit,remark):
        self.equipName=equipName
        self.num=num
        self.unit=unit
        self.remark=remark

    def __str__(self):
        return self.equipName
class Material:
    def __init__(self,materialName,num,unit,remark,state,ratio):
        self.materialName=materialName
        self.num=num
        self.unit=unit
        self.remark=remark
        self.state=state
        self.ratio=ratio
    def __str__(self):
        return  self.materialName
def MaterialJsonToList(data):
    materiallist=[]
    data = json.loads(data)
    for i in range(len(data)):
            materialName=data[i]['materialName']
            num=data[i]['num']
            unit=data[i]['unit']
            remark=data[i]['remark']
            state=data[i]['state']
            ratio=data[i]['ratio']
            material=Material(materialName,num,unit,remark,state,ratio)
            materiallist.append(material)
    return materiallist
def ProductJsonToList(data):
    productlist=[]
    data = json.loads(data)
    for i in range(len(data)):
            productName=data[i]['productName']
            num=data[i]['num']
            unit=data[i]['unit']
            remark=data[i]['remark']
            product=Product(productName,num,unit,remark)
            productlist.append(product)
    return productlist
def EquipJsonToList(data):
    equiplist=[]
    data = json.loads(data)
    for i in range(len(data)):
        equipName = data[i]['equipmentName']
        num = data[i]['num']
        unit = data[i]['unit']
        remark = data[i]['remark']
        equipment = Equipment(equipName, num, unit, remark)
        equiplist.append(equipment)
    return equiplist
def testVBA(request,projectName):
    project = Project.objects.get(projectName=projectName)
    print(projectName)
    equipmentlist = EquipJsonToList(project.equipment)
    materiallist = MaterialJsonToList(project.material)
    productlist = ProductJsonToList(project.product)
    dataComputingMarco(project, equipmentlist, productlist, materiallist)
    return HttpResponse()
def dataComputingMarco(Project,equipmentlist,productlist,materiallist):
    pythoncom.CoInitialize()
    app=xw.App(add_book=False)
    #app = xw.App(visible=False, add_book=False)  # visible是否打开文件
    #app.display_alerts = False
    #app.screen_updating = False

    # 打开xlsm工作簿
    excelName = str(Project.projectName) + '.xlsx'
    #wb = app.books.open(excelName)
    wb=app.books.add()
    wb.sheets.add('数据')
    wb.sheets.add('噪声表')
    wb.sheets.add('废水污染源')
    wb.sheets.add('三表')
    wb.sheets.add('废气信息')
    wb.sheets.add('三同时表')

    '''''
    if wb.sheets['数据'] is None:
        wb.sheets.add('数据')
    if wb.sheets['扩建前废水污染源'] is None:
        wb.sheets.add('扩建前废水污染源')
    if wb.sheets['扩建后废水污染源'] is None:
        wb.sheets.add('扩建后废水污染源')
    if wb.sheets['噪声表'] is None:
        wb.sheets.add('噪声表')
    '''
    #sht = wb.sheets['数据']
    sht=wb.sheets['数据']
    data(sht, Project)

    sht = wb.sheets['废水污染源']

    wastewaterPollutionSourceBeforeExpansion(wb, sht, Project)

    #sht = wb.sheets['扩建后废水污染源']
    #sht = wb.sheets[2]
    #wastewaterPollutionSourceAfterExpansion(wb, sht, Project)

    sht = wb.sheets['噪声表']

    noiseTable(sht, Project)

    threeTable(wb.sheets['三表'],wb.sheets['数据'],Project,equipmentlist,productlist,materiallist)#三表


    SearchGas(wb,materiallist,equipmentlist,Project)#废气检索

    sht=wb.sheets['三同时表']

    threeSameTimeTable(sht,Project,wb,equipmentlist)#三同时表

    fillTable(Project, productlist, wb.sheets['三表'])#填写表格

    wb.save(excelName)
    wb.close()
    app.quit()
def data(sht, Project):
    sht.range('A1').value = "职工不住宿人数(人)"
    sht.range('A2').value = "职工住宿人数(人)"
    sht.range('A3').value = "日工作时间(h)"
    sht.range('A4').value = "年工作时间(d)"
    sht.range('A5').value = "包装袋年产生量(t/a)(固体废物)"
    sht.range('A6').value = "电年耗量(万kWh/a)"
    sht.range('A7').value = "年生活用水量"
    sht.range('A8').value = "日生活用水量"
    sht.range('A9').value = "年生活污水量"
    sht.range('A10').value = "日生活污水量"
    sht.range('A11').value = "生活垃圾年产生量"
    sht.range('A12').value = "生活垃圾日产生量"
    sht.range('A13').value = "边角料年生产量"

    sht.range('B1').value = Project.nonAccommodationNum
    sht.range('B2').value = Project.accommodationNum
    sht.range('B3').value = Project.dayWorkTime
    sht.range('B4').value = Project.yearWorkTime
    sht.range('B5').value = Project.annualSolidWasteOutput
    sht.range('B6').value = Project.annualPowerConsumption
    sht.range('B7').value = (
                                          Project.nonAccommodationNum * 40 + Project.accommodationNum * 80) * Project.yearWorkTime / 1000
    sht.range('B8').value = (Project.nonAccommodationNum * 40 + Project.accommodationNum * 80) / 1000
    sht.range('B9').value = (
                                          Project.nonAccommodationNum * 40 + Project.accommodationNum * 80) * Project.yearWorkTime / 1000 * 0.9
    sht.range('B10').value = (Project.nonAccommodationNum * 40 + Project.accommodationNum * 80) / 1000 * 0.9
    sht.range('B11').value = (
                                           Project.nonAccommodationNum + Project.accommodationNum) * 0.5 * Project.yearWorkTime / 1000
    sht.range('B12').value = (Project.nonAccommodationNum + Project.accommodationNum) * 0.5
    sht.range('B13').value = Project.annualLeftover
# 扩建前废水污染源
def wastewaterPollutionSourceBeforeExpansion(wb, sht, Project):
    # 写表头
    sht.range('A1').value = '类别'
    sht.range('B1').value = '水用量'
    sht.range('C1').value = '水用量'
    sht.range('D1').value = '污水产生量'
    sht.range('E1').value = '污水产生量'
    sht.range('F1').value = '污染物名称'
    sht.range('G1').value = '产生浓度'
    sht.range('H1').value = '产生浓度和数量'
    sht.range('I1').value = '产生浓度和数量'
    sht.range('J1').value = '排放浓度'
    sht.range('K1').value = '排放浓度及排放量'
    sht.range('L1').value = '排放浓度及排放量'
    sht.range('M1').value = '削减量'
    sht.range('N1').value = '削减量'

    # 写单位
    sht.range('B2').value = 'm3/d'
    sht.range('C2').value = 'm3/a'
    sht.range('D2').value = 'm3/d'
    sht.range('E2').value = 'm3/a'
    sht.range('G2').value = 'mg/L'
    sht.range('H2').value = 'kg/d'
    sht.range('I2').value = 't/a'
    sht.range('J2').value = 'mg/L'
    sht.range('K2').value = 'kg/d'
    sht.range('L2').value = 't/a'
    sht.range('M2').value = 'kg/d'
    sht.range('N2').value = 't/a'

    sht.range('F3').value = 'CODcr'
    sht.range('F4').value = 'BOD5'
    sht.range('F5').value = 'NH3-N'
    sht.range('F6').value = 'SS'

    sht.range('G3').value = 250
    sht.range('G4').value = 100
    sht.range('G5').value = 30
    sht.range('G6').value = 100

    # 判断是否入污水厂
    if Project.besideWaterTreatmentPlant == 'False':
        sht.range('J3').value = 100
        sht.range('J4').value = 30
        sht.range('J5').value = 25
        sht.range('J6').value = 30
        sht.range('a25').value = '不入污水厂'
    elif Project.besideWaterTreatmentPlant == 'True':
        sht.range('J3').value = 40
        sht.range('J4').value = 20
        sht.range('J5').value = 8
        sht.range('J6').value = 60
        sht.range('A25').value = '入污水厂'
    else:
        sht.range('J3').value = 0
        sht.range('J4').value = 0
        sht.range('J5').value = 0
        sht.range('J6').value = 0
        sht.range('A25').value = '未知'

    i = 1
    while i <= 4:
        sht.range((i + 2, 1)).value = '生活污水'
        sht.range((i + 2, 2)).value = wb.sheets['数据'].range('B8').value
        sht.range((i + 2, 3)).value = wb.sheets['数据'].range('B7').value
        sht.range((i + 2, 4)).value = wb.sheets['数据'].range('B10').value
        sht.range((i + 2, 5)).value = wb.sheets['数据'].range('B9').value
        #sht.range((i + 2, 2)).value = wb.sheets[0].range('B8').value
        #sht.range((i + 2, 3)).value = wb.sheets[0].range('B7').value
        #sht.range((i + 2, 4)).value = wb.sheets[0].range('B10').value
        #sht.range((i + 2, 5)).value = wb.sheets[0].range('B9').value
        sht.range((i + 2, 8)).value = sht.range((i + 2, 4)).value * sht.range((i + 2, 7)).value / 1000
        sht.range((i + 2, 9)).value = sht.range((i + 2, 5)).value * sht.range((i + 2, 7)).value / 1000 / 1000
        sht.range((i + 2, 11)).value = sht.range((i + 2, 4)).value * sht.range((i + 2, 10)).value / 1000
        sht.range((i + 2, 12)).value = sht.range((i + 2, 5)).value * sht.range((i + 2, 10)).value / 1000 / 1000
        sht.range((i + 2, 13)).value = sht.range((i + 2, 8)).value - sht.range((i + 2, 11)).value
        sht.range((i + 2, 14)).value = sht.range((i + 2, 9)).value - sht.range((i + 2, 12)).value
        i = i + 1

    # TODO: 设置单元格内数字的格式

    # TODO: 设置表格格式

    sht.range('A8').value = '水污染物'
    sht.range('B8').value = '单位'
    sht.range('C8').value = 'mg/L'
    sht.range('D8').value = 'kg/a'
    sht.range('E8').value = 'mg/L'
    sht.range('F8').value = 'kg/a'
    sht.range('G8').value = 't/a'
    sht.range('B9').value = sht.range('F3').value  # CODcr
    sht.range('B10').value = sht.range('F4').value  # BOD5
    sht.range('B11').value = sht.range('F5').value  # NH3-N
    sht.range('C9').value = sht.range('G3').value
    sht.range('C10').value = sht.range('G4').value
    sht.range('C11').value = sht.range('G5').value
    sht.range('E9').value = sht.range('J3').value
    sht.range('E10').value = sht.range('J4').value
    sht.range('E11').value = sht.range('J5').value

    i = 1
    while i <= 3:
        sht.range((i + 8, 4)).value = sht.range((i + 2, 9)).value * 1000
        sht.range((i + 8, 6)).value = sht.range((i + 2, 12)).value * 1000
        i = i + 1

    sht.range('G9').value = sht.range('I3').value
    sht.range('G10').value = sht.range('I4').value
    sht.range('G11').value = sht.range('I5').value

    sht.range('A13').value = '汇总'
    sht.range('A14').value = '排放量及主要污染物'
    sht.range('A15').value = '生活废水'
    sht.range('A16').value = '化学需氧量'
    sht.range('A17').value = '氨氮'
    sht.range('B14').value = '产生量(7)'
    sht.range('C14').value = '自身削减量(8)'
    sht.range('D14').value = '预测排放总量(9)'
    sht.range('E14').value = '核定排放总量(10)'
    sht.range('F14').value = '以新代老削减量(11)'
    sht.range('G14').value = '区域平衡替代本工程削减量(12)'
    sht.range('H14').value = '预测排放总量(13)'
    sht.range('I14').value = '核定排放总量(14)'
    sht.range('J14').value = '排放增减量(15)'

    sht.range('B15').value = sht.range((3, 5)).value / 10000
    sht.range('B16').value = sht.range((3, 9)).value
    sht.range('B17').value = sht.range((5, 9)).value

    sht.range('D15').value = sht.range('B15').value
    sht.range('D16').value = sht.range((3, 12)).value
    sht.range('D17').value = sht.range((5, 12)).value

    i = 1
    while i <= 3:
        '''''
        if sht.range(()):
            sht.range((i + 14, 3)).value = sht.range((i + 14, 2)).value - sht.range((i + 14, 4)).value
            sht.range((i + 14, 5)).value = sht.range((i + 14, 4)).value
            sht.range((i + 14, 6)).value = 0
            sht.range((i + 14, 7)).value = 0
            sht.range((i + 14, 8)).value = sht.range((i + 14, 4)).value
            sht.range((i + 14, 9)).value = sht.range((i + 14, 4)).value
            sht.range((i + 14, 10)).value = sht.range((i + 14, 4)).value
            i = i + 1
        '''''
        sht.range((i + 14, 3)).value = sht.range((i + 14, 2)).value - sht.range((i + 14, 4)).value
        sht.range((i + 14, 5)).value = sht.range((i + 14, 4)).value
        sht.range((i + 14, 6)).value = 0
        sht.range((i + 14, 7)).value = 0
        sht.range((i + 14, 8)).value = sht.range((i + 14, 4)).value
        sht.range((i + 14, 9)).value = sht.range((i + 14, 4)).value
        sht.range((i + 14, 10)).value = sht.range((i + 14, 4)).value
        i = i + 1
        sht.range('A18').value = '计量单位：废水排放量——万吨/年；废气排放量——万标立方米/年；工业固体废物排放量——万吨/年；' \
                                 '水污染物排放浓度——毫克/升；大气污染物排放浓度——毫克/立方米；水污染物排放量——吨/年；' \
                                 '大气污染物排放量—吨/年。'
        sht.range('A20').value = '冷却塔水'
        sht.range('A21').value = '循环冷却水量'
        sht.range('A22').value = '因蒸发损失的水量'
        sht.range('A23').value = '需补充的新鲜水量'

        sht.range('C21').value = 'm3/d'
        sht.range('C22').value = 'm3/d'
        sht.range('C23').value = 'm3/d'
        sht.range('B21').value = 10
        sht.range('B22').value = sht.range('B21').value / 10
        sht.range('B23').value = sht.range('B22')
# 扩建后废水污染源
def wastewaterPollutionSourceAfterExpansion(wb, sht, Project):
    # 写表头
    sht.range('A1').value = '类别'
    sht.range('B1').value = '水用量'
    sht.range('C1').value = '水用量'
    sht.range('D1').value = '污水产生量'
    sht.range('E1').value = '污水产生量'
    sht.range('F1').value = '污染物名称'
    sht.range('G1').value = '产生浓度'
    sht.range('H1').value = '产生浓度和数量'
    sht.range('I1').value = '产生浓度和数量'
    sht.range('J1').value = '排放浓度'
    sht.range('K1').value = '排放浓度及排放量'
    sht.range('L1').value = '排放浓度及排放量'
    sht.range('M1').value = '削减量'
    sht.range('N1').value = '削减量'

    # 写单位
    sht.range('B2').value = 'm3/d'
    sht.range('C2').value = 'm3/a'
    sht.range('D2').value = 'm3/d'
    sht.range('E2').value = 'm3/a'
    sht.range('G2').value = 'mg/L'
    sht.range('H2').value = 'kg/d'
    sht.range('I2').value = 't/a'
    sht.range('J2').value = 'mg/L'
    sht.range('K2').value = 'kg/d'
    sht.range('L2').value = 't/a'
    sht.range('M2').value = 'kg/d'
    sht.range('N2').value = 't/a'

    sht.range('F3').value = 'CODcr'
    sht.range('F4').value = 'BOD5'
    sht.range('F5').value = 'NH3-N'
    sht.range('F6').value = 'SS'

    sht.range('G3').value = 250
    sht.range('G4').value = 100
    sht.range('G5').value = 30
    sht.range('G6').value = 100

    # 判断是否入污水厂
    if Project.besideWaterTreatmentPlant == 'False':
        sht.range('J3').value = 100
        sht.range('J4').value = 30
        sht.range('J5').value = 25
        sht.range('J6').value = 30
        sht.range('a25').value = '不入污水厂'
    elif Project.besideWaterTreatmentPlant == 'True':
        sht.range('J3').value = 40
        sht.range('J4').value = 20
        sht.range('J5').value = 8
        sht.range('J6').value = 60
        sht.range('A25').value = '入污水厂'
    else:
        sht.range('J3').value = 0
        sht.range('J4').value = 0
        sht.range('J5').value = 0
        sht.range('J6').value = 0
        sht.range('A25').value = '未知'

    i = 1
    while i <= 4:
        sht.range((i + 2, 1)).value = '生活污水'
        sht.range((i + 2, 2)).value = wb.sheets['数据'].range('B21').value
        sht.range((i + 2, 3)).value = wb.sheets['数据'].range('B20').value
        sht.range((i + 2, 4)).value = wb.sheets['数据'].range('B23').value
        sht.range((i + 2, 5)).value = wb.sheets['数据'].range('B22').value
        sht.range((i + 2, 8)).value = sht.range((i + 2, 4)).value * sht.range((i + 2, 7)).value / 1000
        sht.range((i + 2, 9)).value = sht.range((i + 2, 5)).value * sht.range((i + 2, 7)).value / 1000 / 1000
        sht.range((i + 2, 11)).value = sht.range((i + 2, 4)).value * sht.range((i + 2, 10)).value / 1000
        sht.range((i + 2, 12)).value = sht.range((i + 2, 5)).value * sht.range((i + 2, 10)).value / 1000 / 1000
        sht.range((i + 2, 13)).value = sht.range((i + 2, 8)).value - sht.range((i + 2, 11)).value
        sht.range((i + 2, 14)).value = sht.range((i + 2, 9)).value - sht.range((i + 2, 12)).value
        i = i + 1

    # TODO: 设置单元格内数字的格式

    # TODO: 设置表格格式

    sht.range('A8').value = '水污染物'
    sht.range('B8').value = '单位'
    sht.range('C8').value = 'mg/L'
    sht.range('D8').value = 'kg/a'
    sht.range('E8').value = 'mg/L'
    sht.range('F8').value = 'kg/a'
    sht.range('G8').value = 't/a'
    sht.range('B9').value = sht.range('F3').value  # CODcr
    sht.range('B10').value = sht.range('F4').value  # BOD5
    sht.range('B11').value = sht.range('F5').value  # NH3-N
    sht.range('C9').value = sht.range('G3').value
    sht.range('C10').value = sht.range('G4').value
    sht.range('C11').value = sht.range('G5').value
    sht.range('E9').value = sht.range('J3').value
    sht.range('E10').value = sht.range('J4').value
    sht.range('E11').value = sht.range('J5').value

    i = 1
    while i <= 3:
        sht.range((i + 8, 4)).value = sht.range((i + 2, 9)).value * 1000
        sht.range((i + 8, 6)).value = sht.range((i + 2, 12)).value * 1000
        i = i + 1

    sht.range('G9').value = sht.range('I3').value
    sht.range('G10').value = sht.range('I4').value
    sht.range('G11').value = sht.range('I5').value

    sht.range('A13').value = '汇总'
    sht.range('A14').value = '排放量及主要污染物'
    sht.range('A15').value = '生活废水'
    sht.range('A16').value = '化学需氧量'
    sht.range('A17').value = '氨氮'
    sht.range('B14').value = '产生量(7)'
    sht.range('C14').value = '自身削减量(8)'
    sht.range('D14').value = '预测排放总量(9)'
    sht.range('E14').value = '核定排放总量(10)'
    sht.range('F14').value = '以新代老削减量(11)'
    sht.range('G14').value = '区域平衡替代本工程削减量(12)'
    sht.range('H14').value = '预测排放总量(13)'
    sht.range('I14').value = '核定排放总量(14)'
    sht.range('J14').value = '排放增减量(15)'

    sht.range('B15').value = sht.range((3, 5)).value / 10000
    sht.range('B16').value = sht.range((3, 9)).value
    sht.range('B17').value = sht.range((5, 9))

    sht.range('D15').value = sht.range('B15').value
    sht.range('D16').value = sht.range((3, 12)).value
    sht.range('D17').value = sht.range((5, 12)).value

    i = 1
    while i <= 3:
        if sht.range(()):
            sht.range((i + 14, 3)).value = sht.range((i + 14, 2)).value - sht.range((i + 14, 4)).value
            sht.range((i + 14, 5)).value = sht.range((i + 14, 4)).value
            sht.range((i + 14, 6)).value = 0
            sht.range((i + 14, 7)).value = 0
            sht.range((i + 14, 8)).value = sht.range((i + 14, 4)).value
            sht.range((i + 14, 9)).value = sht.range((i + 14, 4)).value
            sht.range((i + 14, 10)).value = sht.range((i + 14, 4)).value
            i = i + 1

        sht.range('A18').value = '计量单位：废水排放量——万吨/年；废气排放量——万标立方米/年；工业固体废物排放量——万吨/年；' \
                                 '水污染物排放浓度——毫克/升；大气污染物排放浓度——毫克/立方米；水污染物排放量——吨/年；' \
                                 '大气污染物排放量—吨/年。                                 '
        sht.range('A20').value = '冷却塔水'
        sht.range('A21').value = '循环冷却水量'
        sht.range('A22').value = '因蒸发损失的水量'
        sht.range('A23').value = '需补充的新鲜水量'

        sht.range('C21').value = 'm3/d'
        sht.range('C22').value = 'm3/d'
        sht.range('C23').value = 'm3/d'
        sht.range('B21').value = 10
        sht.range('B22').value = sht.range('B21').value / 10
        sht.range('B23').value = sht.range('B22')
# 噪声表
def noiseTable(sht, Project):
    sht.range('A1').value = "测试编号"
    sht.range('B1').value = "时段"
    sht.range('C1').value = "Leq"
    sht.range('D1').value = "标准"
    sht.range('E1').value = "备注"
    for i in range(Project.noiseMonitoringPoints):
        sht.range('A' + str(2 * i + 2)).value = str(i+1) + ' #'
        sht.range('B' + str(2 * i + 2)).value = '昼'
        sht.range('B' + str(2 * i + 3)).value = '夜'
        sht.range('C' + str(2 * i + 2)).value = random.randint(510,550)/10
        sht.range('C' + str(2 * i + 3)).value = random.randint(390,450)/10
        if Project.soundEnvironmentStandard == '0类':
            sht.range('D' + str(2 * i + 2)).value = '0类 50'
            sht.range('D' + str(2 * i + 3)).value = '0类 40'
        if Project.soundEnvironmentStandard == '1类':
            sht.range('D' + str(2 * i + 2)).value = '1类 55'
            sht.range('D' + str(2 * i + 3)).value = '1类 45'
        if Project.soundEnvironmentStandard == '2类':
            sht.range('D' + str(2 * i + 2)).value = '2类 60'
            sht.range('D' + str(2 * i + 3)).value = '2类 50'
        if Project.soundEnvironmentStandard == '3类':
            sht.range('D' + str(2 * i + 2)).value = '3类 65'
            sht.range('D' + str(2 * i + 3)).value = '3类 55'
        if Project.soundEnvironmentStandard == '4a类':
            sht.range('D' + str(2 * i + 2)).value = '4a类 70'
            sht.range('D' + str(2 * i + 3)).value = '0类 55'
        if Project.soundEnvironmentStandard == '4b类':
            sht.range('D' + str(2 * i + 2)).value = '4b类 70'
            sht.range('D' + str(2 * i + 3)).value = '4b类 60'

        if float(str(sht.range('D' + str(2 * i + 2)).value).split(' ')[-1] )< float(sht.range('C' + str(2 * i + 2)).value):
            sht.range('E' + str(2 * i + 2)).value = '超标'
        else:
            sht.range('E' + str(2 * i + 2)).value = '达标'

        if float(str(sht.range('D' + str(2 * i + 3)).value).split(' ')[-1]) < float(sht.range('C' + str(2 * i + 3)).value):
            sht.range('E' + str(2 * i + 3)).value = '超标'
        else:
            sht.range('E' + str(2 * i + 3)).value = '达标'
def threeTable(sht,data,Project,equipmentlist,productlist,materiallist):
    '''''
    pythoncom.CoInitialize()
    app = xw.App(visible=False, add_book=False)  # visible是否打开文件
    app.display_alerts = False
    app.screen_updating = False

    # 打开xlsm工作簿
    excelName = str(Project.ProjectId) + '.xlsm'
    wb = app.books.open(excelName)

    if wb.sheets['三表'] is None:
        wb.sheets.add('三表')

    sht = wb.sheets['三表']
    '''''
    #wb=app.books.open('新建环评报告_A6.xlsx')
    #wb=xw.Book(r'C:\Users\user\Desktop\项目模板\Web-with-Django\Web-with-Django\web-with-django\SmartEIAproject\新建环评报告_A6.xlsx')
    sht.range('A1').value = '类别'
    sht.range('B1').value = '名称'
    sht.range('C1').value = '单位'
    sht.range('D1').value = '内容'
    sht.range('E1').value = '备注'


    str1: str = ''
    i = 0
    #for r in wb.sheets['产品'].rows:
    '''''
    for r in range(wb.sheets['产品'].api.UsedRange.Rows.count):
        if i == 0:
            continue

        sht.range((i + 1, 2)).value = r[1].value
        sht.range((i + 1, 3)).value = r[2].value
        sht.range((i + 1, 4)).value = r[3].value
        sht.range((i + 1, 5)).value = r[4].value
        sht.range((i + 1, 6)).value = r[5].value
        sht.range((i + 1, 7)).value = r[6].value

        if r[4].value > 0:
            if str1 == '':
                str1 = '年产' + r[1].value + '产品' + r[5].value + r[7].value
            else:
                str1 = str1 + '、' + '年产' + r[1].value + '产品' + r[5].value + r[7].value

        i = i + 1
    '''''
    lr=len(productlist)
    while i <=lr-1:
        sht.range((i + 2, 2)).value = productlist[i].productsName
        sht.range((i + 2, 3)).value = productlist[i].unit
        sht.range((i + 2, 4)).value = productlist[i].num
        sht.range((i + 2, 5)).value = productlist[i].remark
        if str1 == '':
            str1 = '年产' + productlist[i].productsName + '产品' + str(productlist[i].num) + productlist[i].unit.split('/')[0]
        else:
            str1 = str1 + '、' + '年产' + productlist[i].productsName+ '产品' + str(productlist[i].num)+ productlist[i].unit.split('/')[0]
        i=i+1
    i=i+1
    sht.range((2, 1)).value = '产品产量'

    str2: str = ''
    str3: str = ''
    str4: str = ''
    str5: str = ''
    j = 0
    lr=len(equipmentlist)
    #for r in wb.sheets['设备'].rows:
    '''''
    for r in range(wb.sheets['设备'].api.UsedRange.Rows.count):
        if j == 0:
            continue

        sht.range((j + i, 2)).value = r[1].value
        sht.range((j + i, 3)).value = r[2].value
        sht.range((j + i, 4)).value = r[3].value
        sht.range((j + i, 5)).value = r[4].value
        sht.range((j + i, 6)).value = r[5].value
        sht.range((j + i, 7)).value = r[6].value

        if r[4].value > 0:
            if str2 == '':
                str2 = r[1].value + r[4].value + r[2].value
            else:
                str2 = str2 + '、' + r[1].value + r[4].value + r[2].value

        if r[4].value < 0:
            if str3 == '':
                str3 = r[1].value + r[4].value + r[2].value
            else:
                str3 = str3 + '、' + r[1].value + r[4].value + r[2].value

        if r[5].value > 0:
            if str4 == '':
                str4 = r[1].value + r[5].value + r[2].value
            else:
                str5 = str5 + '、' + r[1].value + r[5].value + r[2].value

        if r[3].value > 0:
            if str5 == '':
                str5 = r[1].value + r[3].value + r[2].value
            else:
                str5 = str5 + '、' + r[1].value + r[3].value + r[2].value

        j = j + 1
    '''''
    while j<=lr-1:
        sht.range((j + i+1, 2)).value = equipmentlist[j].equipName
        sht.range((j + i+1, 3)).value = equipmentlist[j].unit
        sht.range((j + i+1, 4)).value = equipmentlist[j].num
        sht.range((j + i+1, 5)).value = equipmentlist[j].remark
        if str2 == '':
            str2 = equipmentlist[j].equipName + str(equipmentlist[j].num) + equipmentlist[j].unit
        else:
            str2 = str2 + '、' +equipmentlist[j].equipName + str(equipmentlist[j].num) + equipmentlist[j].unit
        j=j+1
    sht.range((i + 1, 1)).value = '生产设备'
    j=j+1
    k = 0
    lr=len(materiallist)
    #for r in wb.sheets['材料'].rows:
    '''''
    for r in range(wb.sheets['设备'].api.UsedRange.Rows.count):
        if k == 0:
            continue

        sht.range((i + j + k - 1, 2)).value = r[1].value
        sht.range((i + j + k - 1, 3)).value = r[2].value
        sht.range((i + j + k - 1, 4)).value = r[3].value
        sht.range((i + j + k - 1, 5)).value = r[4].value
        sht.range((i + j + k - 1, 6)).value = r[5].value
        sht.range((i + j + k - 1, 7)).value = r[6].value

        k = k + 1
    '''''
    while k<=lr-1:
        sht.range((i + j + k , 2)).value = materiallist[k].materialName
        sht.range((i + j + k , 3)).value = materiallist[k].unit
        sht.range((i + j + k , 4)).value = materiallist[k].num
        sht.range((i + j + k , 5)).value = materiallist[k].remark
        k=k+1
    #if wb.sheets['信息'].range('B22').value == '无':
    if Project.energyUse=="无":
        sht.range((i + j, 1)).value = '主要原辅材料'
        sht.range((i + j + k , 1)).value = '能源及水耗'
        sht.range((i + j + k , 2)).value = '电'
        sht.range((i + j + k , 3)).value = '万千瓦时/年'
        #sht.range((i + j + k - 1, 4)).value = wb.sheets['数据'].range((6, 2)).value
        #sht.range((i + j + k - 1, 6)).value = wb.sheets['数据'].range((19, 2)).value
        #sht.range((i + j + k - 1, 5)).value = wb.sheets['数据'].range((19, 2)).value - wb.sheets['数据'].range((6, 2)).value
        sht.range((i + j + k , 4)).value=data.range((6,2)).value
        sht.range((i + j + k+1, 2)).value = '生活用水'
        sht.range((i + j + k+1, 3)).value = '立方米/年'
        #sht.range((i + j + k, 4)).value = wb.sheets['数据'].range((7, 2)).value
        #sht.range((i + j + k, 6)).value = wb.sheets['数据'].range((20, 2)).value
        #sht.range((i + j + k, 5)).value = wb.sheets['数据'].range((20, 2)).value - wb.sheets['数据'].range((7, 2)).value
        sht.range((i + j + k+1, 4)).value=data.range((7,2)).value
    sht.range((i + j, 1)).value = '主要原辅材料'
    sht.range((i + j + k , 1)).value = '能源及水耗'
    sht.range((i + j + k , 2)).value = '电'
    sht.range((i + j + k , 3)).value = '万千瓦时/年'
    #sht.range((i + j + k - 1, 4)).value = wb.sheets['数据'].range((6, 2)).value
    sht.range((i + j + k , 4)).value = data.range((6, 2)).value
    #sht.range((i + j + k - 1, 6)).value = wb.sheets['数据'].range((19, 2)).value
    #sht.range((i + j + k - 1, 5)).value = wb.sheets['数据'].range((19, 2)).value - wb.sheets['数据'].range((6, 2)).value
    sht.range((i + j + k+1, 2)).value = '生活用水'
    sht.range((i + j + k+1, 3)).value = '立方米/年'
    #sht.range((i + j + k, 4)).value = wb.sheets['数据'].range((7, 2)).value
    sht.range((i + j + k+1 , 4)).value = data.range((7, 2)).value
    #sht.range((i + j + k, 6)).value = wb.sheets['数据'].range((20, 2)).value
    #sht.range((i + j + k, 5)).value = wb.sheets['数据'].range((20, 2)).value - wb.sheets['数据'].range((7, 2)).value

    #sht.range((i + j + k + 1, 2)).value = wb.sheets['数据'].range('B22').value
    sht.range((i + j + k + 2, 2)).value =Project.energyUse
    sht.range((i + j + k + 2, 3)).value = '立方米/年'

    sht.range((1, 9)).value = str1
    sht.range((2, 9)).value = str2
    Project.constructionScale=str1
    #sht.range((3, 9)).value = str3
    #sht.range((4, 9)).value = str4
    #sht.range((5, 9)).value = str5

    #wb.sheets['信息'].range((23, 2)).value = str1
def threeSameTimeTable(sht,Project,wb,equipmentlist):

    #app = xw.App(visible=False, add_book=False)  # visible是否打开文件
    #app.display_alerts = False
    #app.screen_updating = False
    #wb=app.books.open('新建环评报告_A6.xlsm')
    str1 = ''

    sht.range('A1').value = '类别'
    sht.range('B1').value = '排放源'
    sht.range('C1').value = '污染物名称'
    sht.range('D1').value = '防治措施'
    sht.range('E1').value = '预期处理效果'

    sht.range((2, 1)).value = '水污染物'
    sht.range((2, 2)).value = '生活污水'
    sht.range((2, 3)).value = wb.sheets['废水污染源'].range((9, 2)).value + '、' + wb.sheets['废水污染源'].range((10, 2)).value + '、氨氮'
    #sht.range((2, 4)).value = wb.sheets['信息'].range((42, 2)).value
    sht.range((2, 4)).value='xxxxxx'#待改
    sht.range((2, 5)).value = '达标排放'

    i = 1
    j = 1
    #lr = wb.sheets['废气信息'].rows.count
    lr=7
    while wb.sheets['废气信息'].range((lr+1),1).value!=None and wb.sheets['废气信息'].range((lr+1),1).value!='':
        lr+=1
    print(lr)
    if lr > 7:
        while i <=  lr-7:
            sht.range((i + 2, 2)).value = wb.sheets['废气信息'].range((i + 7, 3)).value
            sht.range((i + 2, 3)).value = wb.sheets['废气信息'].range((i + 7, 4)).value
            sht.range((i + 2, 4)).value = wb.sheets['废气信息'].range((i + 7, 13)).value
            sht.range((i + 2, 5)).value = wb.sheets['废气信息'].range((i + 7, 6)).value
            if str1 == '':
                str1 = sht.range((i + 2, 2)).value + '产生的' + sht.range((i + 2, 3)).value
            else:
                str1 = str1 + '、' + sht.range((i + 2, 2)).value + '产生的' + sht.range((i + 2, 3)).value
            i = i + 1

        # TODO: 设置格式

        sht.range((3, 1)).value = '大气污染物'

    noil = ''
    #lr = wb.sheets['设备'].rows.count
    lr=len(equipmentlist)
    wb.sheets.add('辅助')
    wb.sheets['辅助'].range('a1').value='设备名称'
    for i1 in range(len(equipmentlist)):
        wb.sheets['辅助'].range('a'+str(i1+1)).value=equipmentlist[i1].equipName
    # TODO: ‘辅助’表排序，必做
    #wb.sheets['辅助'].api.Sort()
    if lr == 1:
        noil = ''
    elif lr == 2:
        noil = wb.sheets['辅助'].range((2, 1)).value
    elif lr == 3:
        noil = wb.sheets['辅助'].range((2, 1)).value + wb.sheets['辅助'].range((3, 1)).value
    else:
        noil = wb.sheets['辅助'].range((2, 1)).value +'、'+ wb.sheets['辅助'].range((3, 1)).value + '等'

    lr = wb.sheets['三同时表'].api.UsedRange.Rows.count
    sht.range((lr + 1, 1)).value = '噪声'
    sht.range((lr + 1, 2)).value = noil
    sht.range((lr + 1, 4)).value = '选用低噪声设备，对生产设备进行恰当隔声、减振措施'
    sht.range((lr + 1, 5)).value = '符合《工业企业厂界环境噪声排放标准》（GB12360-2008）中的' + Project.soundEnvironmentStandard+'标准'
                                   #wb.sheets['信息'].range((35, 2)).value + '标准'

    wb.sheets['辅助'].delete()

    sht.range((lr + 2, 1)).value = '固体废物'
    sht.range((lr + 2, 2)).value = '生活垃圾'
    sht.range((lr + 2, 4)).value = '交由环卫部门集中处理'
    sht.range((lr + 3, 2)).value = '边角料、废包装袋'
    sht.range((lr + 3, 4)).value = '卖给废品回收公司'
    sht.range((lr + 2, 5)).value = '符合相应的卫生和环保要求'

    sht.range((lr + 4), 1).value = '生态保护措施及预期效果：' + '\n' + '本项目无需特别的生态保护措施。'
    sht.range((1, 7)).value =str1
    #wb.sheets['信息'].range((24, 2)).value = noil
    Project.noiseEquipment=noil
def SearchGas(wb2,materialList,equipmentList,Project):
    app = xw.App(visible=False, add_book=False)  # visible是否打开文件
    app.display_alerts = False
    app.screen_updating = False
    wb = app.books.open('U:\\新建环评报告_A6.xlsm')
    gaslist=[]
    lr1=len(materialList)
    lr2=len(equipmentList)
    lr3=wb.sheets['废气信息库'].range('F1').expand('table').rows.count#待改
    lr4 = 1
    nogasflag = True
    sht=wb2.sheets['废气信息']
    sht.range((7, 1)).value = '原辅材料'
    sht.range((7, 2)).value = '设备'
    sht.range((7, 3)).value = '工序'
    sht.range((7, 4)).value = '废气污染源名称'
    sht.range((7, 5)).value = '地区'
    sht.range((7, 6)).value = '排放标准'
    sht.range((7, 7)).value = '产污系数'
    sht.range((7, 8)).value = '处理措施（0不用处理）'
    sht.range((7, 9)).value = '收集效率（0代表无组织排放）'
    sht.range((7, 10)).value = '处理效率'
    sht.range((7, 11)).value = '污染源描述'
    sht.range((7, 12)).value = '源影响分析'
    sht.range((7, 13)).value = '防治措施'
    sht.range((7, 14)).value = '材料单位'
    sht.range((7, 15)).value = '数量'
    for i in range(2,lr3+1):
        key1=wb.sheets['废气信息库'].range('a'+str(i)).value
        key2 = wb.sheets['废气信息库'].range('b'+str(i)).value
        key3 = wb.sheets['废气信息库'].range('e'+str(i)).value
        for j in range(lr1):
            if key1 !=None and key1 in materialList[j].materialName :
                for k in range(lr2):
                    if key2 !=None and key2 in equipmentList[k].equipName :
                        if key3 ==None or key3 in Project.township:
                            nogasflag = False
                            print(key1,key2,key3)
                            #lr4=sht.api.UsedRange.Rows.count+1
                            for i1 in range(1,1000):
                                lr4 += 1
                                if sht.range((i1,1)).value!=None and sht.range((i1,1)).value!='':
                                    break
                            sht.range('a'+str(lr4)+':m'+str(lr4)).value=wb.sheets['废气信息库'].range('a'+str(i)+':m'+str(i)).value
                            if wb.sheets['废气信息库'].range('a'+str(i)).value!=None:
                                sht.range('a'+str(lr4)).value=materialList[j].materialName
                                sht.range('n' + str(lr4)).value = materialList[j].unit
                                sht.range('o'+str(lr4)).value=materialList[j].num
                                sht.range('b'+str(lr4)).value=equipmentList[k].equipName
                            else:
                                sht.range('a' + str(lr4)).value = '待填'
                                sht.range('n' + str(lr4)).value = '待填'
                                sht.range('o' + str(lr4)).value = '待填'
                                sht.range('b' + str(lr4)).value = equipmentList[k].equipName
    #lr4=sht.range('A1').expand().last_cell.row#待改
    if(nogasflag == True):
        return 0
    for i in range(8,lr4+1,7):
        print("i is now:"+str(i))
        print(str(lr4+1))
        sht2=wb2.sheets.add(sht.range((i,4)).value)
        gaslist.append(sht.range((i,4)).value)
        sht2.range('a1').value='废气污染源核算'
        sht2.range('a2').value=sht.range('d'+str(i)).value
        sht2.range('b2').value = sht.range('c' + str(i)).value
        #TODO MERGE 'A3:F3'
        sht2.range('a3').value='基本数据'
        sht2.range('a4').value='排气筒高度'
        sht2.range('b4').value = 'm'
        sht2.range('a5').value = '风量'
        sht2.range('b5').value = 'm3/h'
        #TODO B5 m3/h
        #TODO MERGE A6:F6
        sht2.range('a6').value='工作时长'
        sht2.range('a7').value = '年运行天数'
        sht2.range('c7').value = Project.yearWorkTime
        sht2.range('b7').value='d'
        sht2.range('a8').value='日运行时数'
        sht2.range('c8').value=Project.dayWorkTime
        sht2.range('b8').value='h'
        #TODO MERGE A9:F9
        sht2.range('a9').value='效率'
        sht2.range('a10').value = '收集效率'
        sht2.range('a11').value = '去除/处理效率'
        sht2.range('c10').value = sht.range('i'+str(i)).value
        sht2.range('c11').value = sht.range('j' + str(i)).value
        sht2.range('b10').value = '污染物进入集气罩的百分比'
        sht2.range('b11').value = '污染物进入集气罩后经处理设施处理后截留下来的量、速率和浓度'
        sht2.range('a12').value='原材料'
        sht2.range('b12').value = '单位'
        sht2.range('c12').value = '用量'
        sht2.range('e12').value = '系数'
        sht2.range('a13').value=sht.range('a'+str(i)).value
        sht2.range('b13').value = sht.range('n' + str(i)).value
        sht2.range('c13').value = sht.range('o' + str(i)).value
        sht2.range('e13').value = sht.range('g' + str(i)).value

        #有组织排放
        # TODO: 设置格式
        sht2.range('h1').value='有组织排放'
        sht2.range('h2').value='污染物产生量'
        #TODO: MERGE i2:k2
        sht2.range('i2').value = '进入集气罩的情况'
        #TODO: MERGE l2:n2
        sht2.range('l2').value = '排放情况'
        #TODO: MERGE o2:p2
        sht2.range('o2').value = '无组织排放情况'

        sht2.range('h3').value='t/a'
        sht2.range('i3').value = 't/a'
        sht2.range('j3').value = 'kg/h'
        sht2.range('k3').value = 'mg/m3'
        #TODO: 字符上标
        sht2.range('l3').value='t/a'
        sht2.range('m3').value = 'kg/h'
        sht2.range('n3').value = 'mg/m3'
        # TODO: 字符上标
        sht2.range('o3').value='t/a'
        sht2.range('p3').value='kg/h'

        sht2.range('h4').value=str(float(sht2.range('c13').value*float(sht2.range('e13').value)))#待改
        sht2.range('i4').value = str(float(sht2.range('h4').value)*float(sht2.range('c10').value))
        sht2.range('j4').value=str(float(sht2.range('i4').value)*1000/float(sht2.range('c7').value)/float(sht2.range('c8').value))
        #sht2.range('k4').value=str(float(sht2.range('j4').value)*1000*1000/float(sht2.range('c5').value))
        sht2.range('k4').value='待填（[c3]*1000*1000/风量）'
        sht2.range('l4').value=str(float(sht2.range('i4').value)*(1-float(sht2.range('c11').value)))
        sht2.range('m4').value = str(float(sht2.range('j4').value) * (1 - float(sht2.range('c11').value)))
        #sht2.range('n4').value = str(float(sht2.range('k4').value) * (1 - float(sht2.range('c11').value)))
        sht2.range('n4').value ='待填（k4*(1-c11)）'
        sht2.range('o4').value = str(float(sht2.range('h4').value)-float(sht2.range('i4').value))
        sht2.range('p4').value = str(float(sht2.range('o4').value) * 1000 / float(sht2.range('c7').value) / float(sht2.range('c8').value))

        #无组织排放
        # TODO: 设置格式
        sht2.range('h6').value = '无组织排放1'
        sht2.range('h7').value='污染物产生量'
        #TODO: MERGE i7:j7
        sht2.range('i7').value = '进入处理设施情况'
        #TODO: MERGE k7:l7
        sht2.range('k7').value = '削减量'
        #TODO: MERGE m7:n7
        sht2.range('m7').value = '无组织排放总量'

        sht2.range('h8').value='t/a'
        sht2.range('i8').value = 't/a'
        sht2.range('j8').value = 'kg/h'
        sht2.range('k8').value = 't/a'
        sht2.range('l8').value = 'kg/h'
        sht2.range('m8').value='t/a'
        sht2.range('n8').value = 'kg/h'

        sht2.range('h9').value=str(float(sht2.range('c13').value*float(sht2.range('e13').value)))#待改
        sht2.range('i9').value = str(float(sht2.range('h9').value)*float(sht2.range('c10').value))
        sht2.range('j9').value=str(float(sht2.range('i9').value)*1000/float(sht2.range('c7').value)/float(sht2.range('c8').value))
        sht2.range('k9').value=str(float(sht2.range('j9').value)*float(sht2.range('c11').value))
        sht2.range('l9').value=str(float(sht2.range('k9').value)*1000/float(sht2.range('c7').value)/float(sht2.range('c8').value))
        sht2.range('m9').value = str(float(sht2.range('h9').value)-float(sht2.range('k9').value))
        sht2.range('n9').value = str(float(sht2.range('m9').value) * 1000 / float(sht2.range('c7').value) / float(sht2.range('c8').value))

        # 无组织排放2
        sht2.range('h11').value = '无组织排放2'
        sht2.range('h12').value = '原材料用量'
        sht2.range('i12').value = '污染物产生系数'
        sht2.range('j12').value ='最大产生速率'
        sht2.range('k12').value = '产生量'
        sht2.range('l12').value = '排放量'

        sht2.range('h13').value = 'kg/a'
        sht2.range('i13').value = 'g/kg'
        sht2.range('j13').value = 'kg/h'
        sht2.range('k13').value = 'kg/a'
        sht2.range('l13').value = 'kg/a'

        sht2.range('h14').value=str(float(sht2.range('c13').value)*1000)
        sht2.range('i14').value = str(float(sht2.range('e13').value))
        sht2.range('k14').value=str(float(sht2.range('h14').value)*float(sht2.range('i14').value)/1000)
        sht2.range('l14').value=str(float(sht2.range('k14').value))
        sht2.range('j14').value=str(float(sht2.range('k14').value)/float(sht2.range('c7').value)/float(sht2.range('c8').value))
    wb.close()
    app.quit()
    gasjson = []
    for element in gaslist:
        item = {}
        item["gasName"] = element
        item["remark"] = ""
        gasjson.append(item)
    print(str(gasjson))
    newjson = str(gasjson).replace("'",'"')
    print(newjson)
    Project.exhaustGas = newjson
    Project.save()
def fillTable(Project,productlist,threetable):
    #填写表格1
    filePath=os.path.join(os.curdir,'0-基本资料','基础信息表1.xlsx')
    wb=xw.books.open(filePath)
    sht=wb.sheets[0]
    sht.range('d2').value=Project.projectName
    sht.range('d3').value=Project.projectName+Project.constructionScale
    sht.range('d4').value='无'
    sht.range('d5').value=Project.address
    sht.range('d6').value='2'
    sht.range('d7').value=Project.environmentalEffectclassification
    sht.range('d9').value='无'
    sht.range('d10').value='不需开展'
    sht.range('d11').value='无'
    sht.range('e12').value=Project.longtitude
    sht.range('g12').value=Project.latitude
    sht.range('d14').value=Project.totalInvestment
    sht.range('d15').value=Project.projectName
    sht.range('g15').value=Project.corporateName
    sht.range('d16').value=Project.societyCreditcode
    sht.range('g16').value=Project.contacts
    sht.range('d17').value=Project.address
    sht.range('g17').value = Project.telephone
    i=0
    lr=len(productlist)
    strlong=''
    while i<lr:
        strlong=strlong+'建设内容：__'+productlist[i].productsName+'__\n'+\
                '建设规模：__' + str(productlist[i].num)+productlist[i].unit + '__'
        i=i+1
    sht.range('j3').value=strlong
    starttime=datetime.datetime.now()
    sht.range('j6').value=str(str(starttime.year)+'年'+str(starttime.month+1)+'月')
    sht.range('j7').value = str(str(starttime.year) + '年' + str(starttime.month + 3) + '月')
    sht.range('j8').value = Project.NEIType
    sht.range('j9').value = '新申项目'
    sht.range('j10').value = '无'
    sht.range('j11').value = '无'
    sht.range('j14').value=Project.environmentalProtectionInvestment
    sht.range('j15').value =Project.EAcompanyName
    sht.range('m15').value=Project.EAcompanyCertificatenumber
    sht.range('m16').value =Project.EAcompanyTelephone
    sht.range('j17').value = Project.EAcompanyAddress
    wb.save(os.path.join(os.curdir,Project.nameAbbreviation+'-建设项目环评审批基础信息表V1013版.xlsx'))
    wb.close()

    #填写表格2
    filePath=os.path.join(os.curdir,'0-基本资料','基础信息表2.xlsx')
    wb=xw.books.open(filePath)
    shtnew=wb.sheets[0]
    print(shtnew.range('b3').value)
    shtnew.range('d2').value=Project.projectName
    shtnew.range('d3').value=Project.projectName+Project.constructionScale
    shtnew.range('d4').value='无'
    shtnew.range('d5').value=Project.address
    shtnew.range('d6').value='2'
    shtnew.range('d7').value=Project.environmentalEffectclassification
    shtnew.range('d9').value='无'
    shtnew.range('d10').value='不需开展'
    shtnew.range('d11').value='无'
    shtnew.range('e12').value=Project.longtitude
    shtnew.range('g12').value=Project.latitude
    shtnew.range('d14').value=Project.totalInvestment
    shtnew.range('d15').value=Project.projectName
    shtnew.range('g15').value=Project.corporateName
    shtnew.range('d16').value=Project.societyCreditcode
    shtnew.range('g16').value=Project.contacts
    shtnew.range('d17').value=Project.address
    shtnew.range('g17').value = Project.telephone
    i=0
    lr=len(productlist)
    strlong=''
    while i<lr:
        strlong=strlong+'建设内容：__'+productlist[i].productsName+'__\n'+\
                '建设规模：__' + str(productlist[i].num)+productlist[i].unit + '__'
        i=i+1
    shtnew.range('j3').value=strlong
    starttime=datetime.datetime.now()
    shtnew.range('j6').value=str(str(starttime.year)+'年'+str(starttime.month+1)+'月')
    shtnew.range('j7').value = str(str(starttime.year) + '年' + str(starttime.month + 3) + '月')
    shtnew.range('j8').value = Project.NEIType
    shtnew.range('j9').value = '新申项目'
    shtnew.range('j10').value = '无'
    shtnew.range('j11').value = '无'
    shtnew.range('j14').value=Project.environmentalProtectionInvestment
    shtnew.range('j15').value =Project.EAcompanyName
    shtnew.range('m15').value=Project.EAcompanyCertificatenumber
    shtnew.range('m16').value =Project.EAcompanyTelephone
    shtnew.range('j17').value = Project.EAcompanyAddress
    shtnew.range('d36').value=Project.east
    shtnew.range('j36').value=Project.south
    shtnew.range('d37').value=Project.west
    shtnew.range('j37').value = Project.north
    shtnew.range('d38').value=Project.floorSpace
    shtnew.range('j38').value =Project.managementSpace
    shtnew.range('d39').value =Project.businessRange
    shtnew.range('d43').value =threetable.range('i2').value

    wb.save(os.path.join(os.curdir,Project.nameAbbreviation+'-建设项目环评审批基础信息表（导入）V0731.xlsx'))
    wb.close()


