"""Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tests import views

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'logout/$', views.user_logout, name='logout'),  # LOG OUT PAGE
    url(r'^$',views.index, name='index'),
    url(r'register/', views.register, name='register'),  # REGISTRATION PAGE
    url(r'login/', views.user_login, name='login'),  # LOGIN PAGE
    url(r'homepage/$',views.homepage,name='homepage'),
    url(r'^homepage/categories/$',views.categories,name = 'category'),
    url(r'^homepage/categories/(?P<pk>[0-9]+)/$',views.products,name = 'products'),
    url(r'^homepage/categories/products/(?P<pk>[0-9]+)/$', views.singleproduct, name = 'singleproduct'),
    url(r'^homepage/categories/products/productpurchased/(?P<pk>[0-9]+)/$',views.softwarepurchased,name = 'softwarepurchase'),
    url(r'homepage/mysoftwares/$',views.mysoftwares,name='mysoftwares'),
    url(r'homepage/softwares/$',views.allsoftwares,name='allsoftwares'),
    url(r'homepage/categories/products/(?P<pk>[0-9]+)/downloadjar/$',views.macverficationdownload,name = 'downloadjar'),
    url(r'homepage/search/$', views.searchfile, name='search')

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)