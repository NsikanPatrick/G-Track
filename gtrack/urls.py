"""gtrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# NB: Use it this way for the clients => path('', include('gtrack_clients.urls'))
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gtrack_app.urls')),
    path('users', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),

    path("__reload__/", include("django_browser_reload.urls")),
]

# This section allows you to serve media files dynamically on the client from the
# backend by using the url of the media file
# Here you're saying, if settings.DEBUG is True(DEBUG mode is tuned on) then serve media
# files, else don't serve them. But production usually requires debug to be off.
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
