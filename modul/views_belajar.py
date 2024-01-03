from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from akun.models import Users
from modul.models.modul import Module, Pelajaran, Bab, Soal
from modul.models.user import Enroll, UserLatihan, UserPelajaran, UserBab
from modul.utils import bab_navigate, enroll as subscribe
from modul.forms import FormKomentar, CreateModule
from django.contrib import messages
from django.core.exceptions import PermissionDenied

context = {}

def index(request):
    context["kelas"] = Module.objects.all()
    return render(request, 'modul/index.html', context)

def koridor(request, slug):
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
    module = Module.objects.get(slug=slug)
    bab = UserBab.objects.filter(module=module)
    current_bab = Bab.objects.get(module=module, urutan=urutan_bab)
    context['current_bab'] = current_bab
    context['current_pelajaran'] = None
    context['bab'] = bab
    context['slug'] = slug
    context['urutan_bab'] = urutan_bab
    context['prev'] = UserPelajaran.objects.get(user=request.user, pelajaran=current_bab.getPelajaran().latest('urutan')) 
    context['halaman'] = 'rangkuman'
    context['current'] = None
    return render(request, 'modul/belajar/rangkuman.html', context)

def koridor_soal(request, slug, urutan_bab):
    context['halaman'] = 'koridor'
    pass


# Teacher Area

def create(request, slug):
    if slug != 'new':
        module = get_object_or_404(Module, slug=slug)

    if request.method == 'POST':
        form = CreateModule(request.POST, request.FILES, request=request) if slug == 'new' else CreateModule(request.POST, request.FILES,request=request, instance=module)
        if form.is_valid():
            module = form.save()
            if module:
                messages.success(request, "Berhasil menambahkan Module Kelas")
            else:
                messages.error(request, "Gagal menambahkan module Kelas")
            return redirect('modul:index')
    else:
        form = CreateModule() if slug == 'new' else CreateModule(instance=module)
    return render(request, 'modul/create.html', {'form':form})

def hapus(request):
    if request.method == "POST":
        slug = request.POST['slug']
        modul = Module.objects.get(slug=slug)
        messages.success(request, f'Kelas {modul.nama} berhasil dihapus')
        modul.delete()
        return redirect('modul:index')
    return redirect('modul:index')

# def edit(request, slug):
#     module = get_object_or_404(Module, slug=slug)

#     if request.method == 'POST':
#         form = CreateModule(request.POST, request.FILES, instance=module)
#         if form.is_valid():
#             user = request.user if request.user.is_authenticated else None
#             module = form.save(user=user)
#             if module:
#                 messages.success(request, "Berhasil Mengedit Module Kelas")
#             else:
#                 messages.error(request, "Gagal Mengedit module Kelas")
#             return redirect('modul:index')
#     else:
#         form = CreateModule(instance=module)
#     return render(request, 'modul/create.html', {'form':form})