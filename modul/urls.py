from django.urls import path
from . import views_belajar

urlpatterns = [
    path('', views_belajar.index, name="index"),
    path('<str:slug>', views_belajar.koridor, name="koridor"),
    path('<str:slug>/<int:urutan_bab>/koridor', views_belajar.koridor, name="koridor"),
    path('<str:slug>/<int:urutan_bab>/rangkuman', views_belajar.rangkuman, name="rangkuman"),
    path('<str:slug>/<int:urutan_bab>/koridor_soal', views_belajar.koridor_soal, name="koridor_soal"),
    path('<str:slug>/<int:urutan_bab>/<int:urutan_pelajaran>', views_belajar.modul, name="modul"),
    path('subscribe/<str:slug>', views_belajar.index , name="subscribe"),
]