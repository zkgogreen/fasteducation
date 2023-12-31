from django.shortcuts import render, redirect
from django.views import View
from akun.models import Users
from modul.models.modul import Module, Pelajaran, Bab
from modul.models.user import Enroll, UserLatihan, UserPelajaran, UserBab
from modul.utils import bab_navigate
from modul.forms import FormKomentar

context = {}
# Create your views here.
class index(View):
    def get(self, request, slug=None):
        if not slug:
            context["kelas"] = Module.objects.all()
            return render(request, 'modul/index.html', context)

        else:
            module = Module.objects.get(slug=slug)
            enroll = Enroll.objects.filter(user=request.user, module=module)
            lesson = UserPelajaran.objects.filter(user=request.user, module=module)
            if not enroll.exists():
                Enroll.objects.create(user=request.user, module=module)
                return redirect("modul:koridor", slug=slug)
            context["user"] = Users.objects.get(user=request.user)
            context["kelas"] = module
            context["enroll"] = enroll[0]
            context['history'] = enroll.first() if enroll.exists() else None
            context["pelajaran"] = str(lesson.filter(isdone=True).count()) + " / " + str(Pelajaran.objects.filter(module=module).count())
            context['latihan']      = UserLatihan.objects.filter(module=module, user=request.user)
            return render(request, 'modul/koridor.html', context)
        
    def post(self, request, slug):
        module = Module.objects.get(slug=slug)
        pelajaran = Pelajaran.objects.filter(module=module).order_by("urutan")
        bab = Bab.objects.filter(module=module).order_by("urutan")

        enroll = Enroll.objects.filter(user=request.user, module=module)

        enroll.update(enroll=True, user=request.user, module=module, bab_module=bab.first(), pelajaran=pelajaran.filter(bab_module=bab.first()).first())
        for i in pelajaran:
            UserPelajaran.objects.create(enroll=enroll.first(), user=request.user, module=module, pelajaran=i, bab_module=i.bab_module)
        for i in bab:
            UserBab.objects.create(enroll=enroll.first(), user=request.user, module=module, bab_module=i)
        return redirect("modul:koridor", slug=slug)
    
class pelajaran(View):
    def get(self, request, slug , bab, pelajaran):
        context.update(bab_navigate(request, slug, bab, pelajaran))
        context['slug'] = slug
        context['urutan_bab'] = bab
        context['pelajaran'] = pelajaran
        context['halaman'] = 'pelajaran'
        context['FormKomentar'] = FormKomentar()
        return render(request, 'modul/pelajaran/pelajaran.html', context)

    def post(self, request, id_pelajaran):
        pelajaran = Pelajaran.objects.get(id=id_pelajaran)
        form = FormKomentar(request.POST)

        if form.is_valid():
            komentar = form.cleaned_data  # Create a model instance from the form data
            komentar.kelas = pelajaran.kelas
            komentar.pelajaran = pelajaran
            komentar.user = request.user
            komentar.save()  # Save the model instance to the database

        return redirect("user:pelajaran", slug=pelajaran.slug, bab=pelajaran.bab_kelas.urutan, pelajaran=pelajaran.urutan)
    

def rangkuman(request, slug, bab):
    module = Module.objects.get(slug=slug)
    bab = Bab.objects.filter(module=module)
    nextbab = bab.filter(urutan=bab + 1)
    jum_pelajaran = Pelajaran.objects.filter(bab_module=bab.get(urutan=bab)).count()
    context.update(bab_navigate(request, slug, bab, jum_pelajaran, False))
    context['halaman'] = 'rangkuman'
    context['nextbab'] = nextbab.first() if nextbab.exists() else None
    return render(request, 'modul/pelajaran/rangkuman.html', context)


def koridor_soal(request, slug, urutan_bab):
    module = Module.objects.get(slug=slug)
    bab = Bab.objects.filter(module=module)
    nextbab = bab.filter(urutan=urutan_bab+1)
    jum_pelajaran = Pelajaran.objects.filter(bab_module=bab.get(urutan=urutan_bab)).count()
    context.update(bab_navigate(request, slug, urutan_bab, jum_pelajaran, False))
    context['halaman'] = 'soal'
    context['nextbab'] = nextbab.first() if nextbab.exists() else None
    context['nilai'] = UserLatihan.objects.filter(user=request.user, bab_module=bab.get(urutan=urutan_bab)).order_by( "-id")
    return render(request, 'modul/pelajaran/koridor_soal.html', context)

def rangkuman_kelas(request, slug):
    module  = Module.objects.get(slug=slug)
    bab = UserBab.objects.filter(user=request.user, module=module)
    history = Enroll.objects.get(module=module, user=request.user)
    context['history'] = history
    context['bab'] = bab
    context['babprev'] = bab[bab.count()-1]
    context['kelas']   = module
    context['halaman'] = 'rangkumankelas'
    return render(request, 'user/kelas/pelajaran/rangkuman.html', context)