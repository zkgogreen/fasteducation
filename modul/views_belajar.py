from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from akun.models import Users
from modul.models.modul import Module, Pelajaran, Bab, Soal
from modul.models.user import Enroll, UserLatihan, UserPelajaran, UserBab
from modul.utils import bab_navigate, enroll as subscribe
from modul.forms import FormKomentar, CreateModule, CreateBab, CreatePelajaran
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def index(request):
    context = {}
    context["kelas"] = Module.objects.all()
    return render(request, 'modul/index.html', context)

def koridor(request, slug):
    context = {}
    module = Module.objects.get(slug=slug)
    enroll = Enroll.objects.filter(user=request.user, module=module)
    context['slug'] = slug
    context['module'] = module
    context['enroll'] = enroll.first()
    if not enroll.exists():
        Enroll.objects.create(user=request.user, module=module)
        return redirect("modul:koridor", slug=slug)
    
    if request.method == "POST":
        enrollMessage = subscribe(request, slug)
        messages.success(request, "anda berhasil mendaftar di "+enrollMessage.nama)
        return redirect("modul:koridor", slug=slug)
    return render(request, 'modul/koridor.html', context)

def modul(request, slug, urutan_bab, urutan_pelajaran):
    context = {}
    context.update(bab_navigate(request, slug, urutan_bab, urutan_pelajaran))
    pelajaran = UserPelajaran.objects.get(user=request.user, module=context['modul'], bab_module=context['current_bab'], pelajaran=context['current_pelajaran'])
    if not pelajaran.allow_next():
        context['forbidden'] = True
        return render(request, 'modul/belajar/forbidden.html', context)
    if request.method == "POST":
        soal = Soal.objects.get(id=request.POST['id'])
        if soal.answer == request.POST['jawaban']:
            messages.success(request, soal.penjelasan)
            UserPelajaran.objects.filter(user=request.user, module=context['modul'], bab_module=context['current_bab'], pelajaran=context['current_pelajaran']).update(isdone=True)
            if context['next']:
                return redirect('modul:modul', slug=slug, urutan_bab=urutan_bab, urutan_pelajaran=urutan_pelajaran+1)
            else:
                return redirect('modul:rangkuman', slug=slug, urutan_bab=urutan_bab)
        else:
            messages.error(request, soal.penjelasan)
        return redirect('modul:modul', slug=slug, urutan_bab=urutan_bab, urutan_pelajaran=urutan_pelajaran)
    return render(request, 'modul/belajar/index.html', context)

def rangkuman(request, slug, urutan_bab):
    context = {}
    module = Module.objects.get(slug=slug)
    bab = UserBab.objects.filter(module=module)
    current_bab = Bab.objects.get(module=module, urutan=urutan_bab)
    context['current_bab'] = current_bab
    context['current_pelajaran'] = None
    context['bab'] = bab
    context['slug'] = slug
    context['urutan_bab'] = urutan_bab
    context['prev'] = UserPelajaran.objects.get(user=request.user, pelajaran=current_bab.getPelajaran().latest('urutan')) if bab.exists() else None
    context['halaman'] = 'rangkuman'
    context['current'] = None
    return render(request, 'modul/belajar/rangkuman.html', context)

def koridor_soal(request, slug, urutan_bab):
    context = {}
    context['halaman'] = 'koridor'
    pass
