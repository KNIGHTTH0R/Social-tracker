"""SocialCounter URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from Account import views as profile_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^register/',profile_views.register),
	url(r'^login/',profile_views.login),
    url(r'^logout/',profile_views.logout),
    url(r'^$',profile_views.accountadd),
    url(r'^instagram/(?P<susername>[\w.@+-]+)',profile_views.accountadd),
	url(r'^twitter/(?P<susername>[\w.@+-]+)',profile_views.accountadd)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)