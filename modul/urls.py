from django.urls import path
from . import views_belajar, views_edit_belajar

urlpatterns = [
    path('', views_belajar.index, name="index"),

    # kelas
    # path('<str:slug>/create', views_edit_belajar.create, name="create"), #create | edit
    # path('edit/delete/hapus', views_edit_belajar.hapus, name="hapus"),
    path('edit/<str:slug>/<str:action>', views_edit_belajar.ModuleView.as_view(), name="module"),
    path('edit/<str:slug>/bab/<str:pk>/<str:action>', views_edit_belajar.BabView.as_view(), name="bab"),

    # path('edit/bab/<str:pk>', views_edit_belajar.bab, name="bab"),
    # path('edit/<str:slug>/bab_form/<str:action>', views_edit_belajar.BabView.as_view(), name="bab_create"),
    # path('edit/<str:slug>/bab_form/<str:action>/<str:pk>', views_edit_belajar.BabView.as_view(), name="bab_edit"),

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