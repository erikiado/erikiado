"""erikiado URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from .views import home, piradio, muestrame, tosp, znake, life, manos, tianguis, msl, classifier_upload
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

projects = [
    url(r'^piradio/', piradio, name='piradio'),
    url(r'^muestrame/', muestrame, name='muestrame'),
    url(r'^tosp/', tosp, name='tosp'),
    url(r'^tianguis/', tianguis, name='tianguis'),
    url(r'^manos/', manos, name='manos'),
    url(r'^znake/', znake, name='znake'),
    url(r'^life/', life, name='life'),
    url(r'^msl/', msl, name='msl'),
]


classifier = [
    url(r'^upload/', classifier_upload, name='classifier_upload'),
]


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^projects/', include(projects)),
    url(r'^classifier/', include(classifier)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



urlpatterns += staticfiles_urlpatterns()