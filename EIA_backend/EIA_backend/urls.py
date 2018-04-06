"""EIA_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.documentation import include_docs_urls
from django.conf.urls import url, include
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from users.views import UserViewset
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from company.views import CompanyViewSet, MembershipViewSet
from projects.views import ProjectViewSet,ProjectFileViewset
from utils import VBA,DocGenTest,Updownload
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

router.register(r'user', UserViewset, base_name="user")

router.register(r'company', CompanyViewSet, base_name="company")

router.register(r'project', ProjectViewSet, base_name="project")

router.register(r'membership', MembershipViewSet, base_name="membership")

router.register(r'projectFile',ProjectFileViewset, base_name="projectFile")

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='My API title')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/', include(router.urls)),

    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),

    # drf 自带auth
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api/VBA/create/(?P<projectName>[\u4e00-\u9fa5_a-zA-Z0-9_]+)/$', VBA.testVBA , name='testVBA'),
    url(r'^api/Word/create/(?P<projectName>[\u4e00-\u9fa5_a-zA-Z0-9_]+)/$', DocGenTest.createWord , name='createWord'),
    url(r'^api/updownload/(?P<projectName>[\u4e00-\u9fa5_a-zA-Z0-9_]+)/(?P<filetype>[0-9]+)/(?P<operation>[0-9]+)/$', Updownload.fileDealing , name='upDownload'),
    # jwt auth
    url(r'^login/', obtain_jwt_token),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
