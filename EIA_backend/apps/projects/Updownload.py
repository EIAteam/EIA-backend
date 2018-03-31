from django.http import HttpResponse
import os
from django.http import StreamingHttpResponse
from .models import Project

def getfileextension(s):
    i = len(s) - 1
    while(s[i]!='.'):
        i = i - 1;
    i = len(s) - i
    return s[-1*i:]

def download(name,exceldir):
    filename = os.path.join(exceldir, name) # 显示在弹出对话框中的默认的下载文件名
    print(filename)
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)
    return response



def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break


def upload(request, exceldir, name):
    if request.POST:
        i = 1
        while(i<=3):
            file_obj = request.FILES.getlist('img'+str(i))
            j = 1
            for f in file_obj:
                filename = os.path.join(exceldir,name)
                if not os.path.isdir(exceldir):
                    os.makedirs(exceldir)
                fobj = open(filename, 'wb')
                for chrunk in f.chunks():
                    fobj.write(chrunk)
                fobj.close()
                j = j + 1
            i = i + 1
        return HttpResponse("success")
    else:
        return HttpResponse("error")
def fileDealing(request,projectName,filetype,operation):
    print("entered")
    project = Project.objects.get(projectName=projectName)
    exceldir = os.path.join('C:\\文件库', 'Projects', 'Company' + str(project.company_id), projectName)
    if not os.path.isdir(exceldir):
        os.makedirs(exceldir)
    if(operation=="1"): #上传
        if (filetype == "1"):
            upload(request, exceldir, projectName+"(初稿).docx")
        elif (filetype == "2"):
            upload(request, exceldir, projectName + ".xlsm")
        elif (filetype == "3"):
            upload(request, exceldir, projectName + "(终稿).docx")
    if(operation=="2"): #下载
        if(filetype=="1"):
            download(projectName+"(初稿).docx",exceldir)
        elif(filetype=="2"):
            download(projectName + ".xlsm", exceldir)
        elif(filetype=="3"):
            download(projectName + "(终稿).docx", exceldir)
    return HttpResponse("success")