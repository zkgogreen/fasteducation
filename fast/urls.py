
from django.contrib import admin
from django.urls import path, include
from . import begin, views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", views.index, name='index'),
    path("home", views.home, name='home'),
    path("begin/", begin.begin, name='begin'),
    path('kelas/', include(('kelas.urls', 'kelas'), namespace='kelas')),
    path('modul/', include(('modul.urls', 'modul'), namespace='modul')),
    path('pesan/', include(('pesan.urls', 'pesan'), namespace='pesan')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
