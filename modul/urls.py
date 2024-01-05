from django.urls import path
from . import views_belajar, views_edit_belajar

urlpatterns = [
    path('', views_belajar.index, name="index"),

    # kelas
    path('edit/create/<str:slug>', views_edit_belajar.create, name="create"), #create | edit
    path('edit/delete/hapus', views_edit_belajar.hapus, name="hapus"),

    path('edit/bab/<str:pk>', views_edit_belajar.bab, name="bab"),
    path('edit/bab_form/<str:slug>/<str:action>', views_edit_belajar.BabView.as_view(), name="bab_form"),
    path('edit/pelajaran/<str:slug>', views_edit_belajar.pelajaran, name="pelajaran"),

    #pelajaran
    path('edit/pelajaran_edit/<int:bab_id>/<str:pelajaran>', views_edit_belajar.pelajaran_edit, name="pelajaran_edit"),
    path('edit/pelajaran_tambah/<int:bab_id>/<str:pelajaran>', views_edit_belajar.pelajaran_tambah, name="pelajaran_tambah"),

    path('<str:slug>', views_belajar.koridor, name="koridor"),
    path('<str:slug>/<int:urutan_bab>/koridor', views_belajar.koridor, name="koridor"),
    path('<str:slug>/<int:urutan_bab>/rangkuman', views_belajar.rangkuman, name="rangkuman"),
    path('<str:slug>/<int:urutan_bab>/koridor_soal', views_belajar.koridor_soal, name="koridor_soal"),
    path('<str:slug>/<int:urutan_bab>/<int:urutan_pelajaran>', views_belajar.modul, name="modul"),
    path('subscribe/<str:slug>', views_belajar.index , name="subscribe"),

]