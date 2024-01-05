from django.shortcuts import render, redirect, get_object_or_404
from modul.models.modul import Module, Bab, Pelajaran
from modul.forms import CreateBab, CreateModule, CreatePelajaran
from django.contrib import messages
from django.views import View

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


class BabView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.module = Module.objects.get(slug=kwargs['slug'])
        self.instance = Bab.objects.get(id=kwargs['action']) if "create" not in kwargs['action'] else ""
        self.context = {
            'babs':Bab.objects.filter(module=self.module),
            'slug':kwargs['slug']
        }


    def get(self, request, *args, **kwargs):
        self.context['form'] = CreateBab() if kwargs['action'] == 'create' else CreateBab(instance=Bab.objects.get(id=kwargs['action'])) 
        return render(request, 'modul/edit/bab_form.html', self.context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CreateBab(request.POST) if kwargs['action'] == 'new' else CreateBab(request.POST, instance=self.instance)
            if form.is_valid():
                bab_instance = form.save(commit=False)
                bab_instance.module = self.instance.module
                bab_instance.save()
                return redirect('modul:bab', pk=self.instance.id)
        else:
            form = CreateBab() if self.pk == 'new' else CreateBab(request.POST, instance=self.instance)
        self.context['form'] = form
        return render(request, 'modul/edit/bab_form.html', self.context)
    
def bab(request, pk):
    bab = Bab.objects.get(id=pk)
    context = {
        'babs':Bab.objects.filter(module=bab.module),
        'bab':bab,
        'slug':bab.module.slug
    }
    return render(request, 'modul/edit/bab.html', context)


# def bab(request, id):
#     bab = Bab.objects.get(id=id)
#     module = bab.module
#     context = {}
#     context['bab'] = Bab.objects.filter(module=module).order_by('urutan')
#     context['slug'] = module.slug
#     return render(request, 'modul/edit/bab.html', context)


# def bab_form(request, slug, action):
#     module = Module.objects.get(slug=slug)
#     if request.method == 'POST':
#         form = CreateBab(request.POST) if action == 'new' else CreateBab(request.POST, instance=Bab.objects.get(id=action))
#         if form.is_valid():
#             bab_instance = form.save(commit=False)
#             bab_instance.module = module
#             bab_instance.save()
#             return redirect('modul:edit', slug=slug)
#     else:
#         form = CreateBab() if action == 'new' else CreateBab(request.POST, instance=Bab.objects.get(id=action))
#     context = {}
#     context['bab'] = Bab.objects.filter(module=module).order_by('urutan')
#     context['slug'] = slug
#     context['form'] = form
#     return render(request, 'modul/edit/bab_form.html', context)


def pelajaran(request, slug):
    module = Module.objects.get(slug=slug)
    if request.method == 'POST':
        form = CreateBab(request.POST)
        
        if form.is_valid():
            bab_instance = form.save(commit=False)
            bab_instance.module = module
            bab_instance.save()
            return redirect('modul:edit', slug=slug)
    else:
        form = CreateBab()
    context = {}
    context['module'] = module
    context['bab'] = Bab.objects.filter(module=module).order_by('urutan')
    context['slug'] = slug
    context['form'] = form
    return render(request, 'modul/edit/index.html', context)

def pelajaran_edit(request, bab_id, pelajaran):
    bab = Bab.objects.get(id=bab_id)
    context = {
        'slug':bab.module.slug,
        'pelajaran':Pelajaran.objects.get(id=pelajaran),
        'bab':Bab.objects.filter(module=bab.module).order_by('urutan')
    }
    return render(request, 'modul/edit/pelajaran.html', context)

def pelajaran_tambah(request, bab_id, pelajaran):
    bab = Bab.objects.get(id=bab_id)
    if request.method == 'POST':
        form = CreatePelajaran(request.POST) if pelajaran == "new" else CreatePelajaran(request.POST, instance=Pelajaran.objects.get(id=pelajaran))
        if form.is_valid():
            pelajaranForm = form.save(commit=False)
            pelajaranForm.module = bab.module
            pelajaranForm.bab_module = bab
            pelajaranForm.urutan = Pelajaran.objects.filter(bab_module=bab).count() + 1
            pelajaranForm.save()
            return redirect('modul:edit', slug=bab.module.slug)
    else:
        form = CreatePelajaran() if pelajaran == "new" else CreatePelajaran(instance=Pelajaran.objects.get(id=pelajaran))
    context = {
        'form':form,
        'slug':bab.module.slug,
        'bab':Bab.objects.filter(module=bab.module).order_by('urutan')
    }
    return render(request, 'modul/edit/pelajaran_edit.html', context)