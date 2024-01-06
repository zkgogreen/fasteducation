from django.shortcuts import render, redirect, get_object_or_404
from modul.models.modul import Module, Bab, Pelajaran
from modul.forms import CreateBab, CreateModule, CreatePelajaran, EditModule
from django.contrib import messages
from django.views import View

class ModuleView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.module = Module.objects.get(slug=kwargs['slug']) if kwargs['slug'] != "new" else None
        self.slug = kwargs['slug'] or None
        self.context = {
            'slug':self.slug,
            'babs':Bab.objects.filter(module=self.module),
            'module':self.module
        }

    def get(self, request, *args, **kwargs):
        if kwargs['action'] == "read":
            return render(request, 'modul/edit/index.html', self.context)
        if kwargs['action'] == "create":
            self.context['form'] = CreateModule()
            return render(request, 'modul/create.html', self.context)
        if kwargs['action'] == "edit":
            self.context['form'] = EditModule(instance=self.module)
            return render(request, 'modul/edit/module_form.html', self.context)
        if kwargs['action'] == "delete":
            nama = self.module.nama
            self.module.delete()
            messages.success(request, f"Berhasil Menghapus kelas {nama}")
            return redirect("modul:index")
        
    def post(self, request, *args, **kwargs):
        if kwargs['action'] == "edit":
            form = EditModule(request.POST, request.FILES,instance=self.module)
            if form.is_valid():
                form.save()
                messages.success(request, f"Berhasil Mengedit kelas {self.module.nama}")
                return redirect('modul:module', slug=self.slug, action="read")
            
        if kwargs['action'] == "create":
            form = CreateModule(request.POST, request.FILES, request=request)
            if form.is_valid():
                messages.success(request, f"Berhasil menambah kelas {request.POST['nama']}")
                form.save()
                return redirect('modul:index')

class BabView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.module = Module.objects.get(slug=kwargs['slug'])
        self.slug = kwargs['slug']
        self.instance = Bab.objects.get(id=kwargs['pk']) if kwargs['pk'] != 'new' else None
        self.context = {
            'bab':Bab.objects.get(id=kwargs['pk']) if kwargs['pk'] != 'new' else None,
            'babs':Bab.objects.filter(module=self.module),
            'slug':kwargs['slug']
        }

    def get(self, request, *args, **kwargs):
        if kwargs['action'] == "read":
            self.context['bab'] = Bab.objects.get(id=kwargs['pk'])
            return render(request, 'modul/edit/bab.html', self.context)
        if kwargs['action'] == "create":
            self.context['form'] = CreateBab()
            return render(request, 'modul/edit/bab_form.html', self.context)
        if kwargs['action'] == "edit":
            self.context['form'] = CreateBab(instance=self.module)
            return render(request, 'modul/edit/bab_form.html', self.context)
        if kwargs['action'] == "delete":
            nama = self.module.nama
            self.module.delete()
            messages.success(request, f"Berhasil Menghapus kelas {nama}")
            return redirect("modul:index")

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CreateBab(request.POST) if kwargs['action'] == 'create' else CreateBab(request.POST, instance=self.instance)
            if form.is_valid():
                bab_instance = form.save(commit=False)
                bab_instance.module = self.module
                bab_instance.save()
                return redirect('modul:bab', slug=self.slug,  pk=bab_instance.id, action="read")
        else:
            form = CreateBab() if self.pk == 'create' else CreateBab(request.POST, instance=self.instance)
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
    context['babs'] = Bab.objects.filter(module=module).order_by('urutan')
    context['slug'] = slug
    context['form'] = form
    return render(request, 'modul/edit/index.html', context)

def pelajaran_edit(request, bab_id, pelajaran):
    bab = Bab.objects.get(id=bab_id)
    context = {
        'slug':bab.module.slug,
        'pelajaran':Pelajaran.objects.get(id=pelajaran),
        'babs':Bab.objects.filter(module=bab.module).order_by('urutan')
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
        'babs':Bab.objects.filter(module=bab.module).order_by('urutan')
    }
    return render(request, 'modul/edit/pelajaran_edit.html', context)