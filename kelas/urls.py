from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('jadwal', views.jadwal, name="jadwal"),
    path('upgrade', views.upgrade, name="upgrade"),
    path('confirm/<int:id>', views.confirm, name="confirm"),
    path('thank', views.thank, name="thank"),
    path('pertemuan', views.pertemuan, name="pertemuan"),
    path('premium', views.premium, name="premium"),
]