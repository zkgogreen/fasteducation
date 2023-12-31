from modul.models.user import Enroll, UserBab, UserPelajaran, UserQuestion
from modul.models.modul import Module, Bab, Pelajaran, Soal


def bab_navigates(request, slug, urutan_bab, urutan_pelajaran, isPelajaran=True):
    context = {}
    module = Module.objects.get(slug=slug)
    bab = Bab.objects.filter(module=module)
    pelajarans = Pelajaran.objects.filter(module=module)
    history = Enroll.objects.get(module=module, user=request.user)

    current = pelajarans.get(urutan=urutan_pelajaran, bab_module=bab.get(urutan=urutan_bab))
    current_bab = bab.get(urutan=urutan_bab)

    userlesson = UserPelajaran.objects.filter(user=request.user, module=module, bab_module=current.bab_module)
    userbab = UserBab.objects.filter(user=request.user, module=module)

    hasPrev = pelajarans.filter(bab_module=current_bab.urutan, urutan=urutan_pelajaran-1)
    hasNext = pelajarans.filter(bab_module=current_bab.urutan, urutan=urutan_pelajaran+1)
    context['bab'] = userbab
    context['hasPrev'] = hasPrev.first() if hasPrev.exists() else current_bab
    context['hasNext'] = hasNext.first() if hasNext.exists() else bab.get(urutan=urutan_bab+1) if bab.filter(urutan=urutan_bab+1).exists() else False
    context['pelajaran'] = current
    context['history'] = history
    context['soal'] = Soal.objects.filter(lesson=current)
    context['komentar'] =  UserQuestion.objects.filter(bab_module=current_bab)

    userlesson.filter(pelajaran=current).update(isdone=True)
    history.bab_module = current.bab_module
    history.pelajaran = current
    history.save()

    return context

def bab_navigate(request, slug, urutan_bab=None, urutan_pelajaran=None):
    context = {}
    modul = Module.objects.get(slug=slug)
    current_bab = Bab.objects.get(module=modul, urutan=urutan_bab)
    current_pelajaran = Pelajaran.objects.get(module=modul, bab_module=current_bab, urutan=urutan_pelajaran)

    pelajaran = Pelajaran.objects.filter(module=modul, bab_module=current_bab)
    bab = UserBab.objects.filter(module=modul)
    babs = Bab.objects.filter(module=modul)
    Enroll.objects.filter(user=request.user, module=modul).update(pelajaran=current_pelajaran, bab_module=current_bab)

    next = UserPelajaran.objects.get(user=request.user, pelajaran=pelajaran.get(urutan=urutan_pelajaran + 1)) if pelajaran.filter(urutan=urutan_pelajaran + 1).exists() else None
    prev = UserPelajaran.objects.get(user=request.user,pelajaran=pelajaran.get(urutan=urutan_pelajaran - 1)) if pelajaran.filter(urutan=urutan_pelajaran - 1).exists() else None

    next_bab = babs.get(urutan=urutan_bab+1) if not pelajaran.filter(urutan=urutan_pelajaran + 1).exists() and babs.filter(urutan=urutan_bab+1).exists() else None
    prev_bab = babs.get(urutan=urutan_bab-1) if not pelajaran.filter(urutan=urutan_pelajaran - 1).exists() and babs.filter(urutan=urutan_bab-1).exists() else None
    enroll = Enroll.objects.get(user=request.user, module=modul)
    context['modul'] = modul
    context['enroll'] = enroll
    context['current'] = UserPelajaran.objects.get(enroll=enroll, pelajaran=current_pelajaran) 
    context['slug'] = slug
    context['bab'] = bab
    context['pelajaran'] = current_pelajaran
    context['next'] = next
    context['prev'] = prev
    context['next_bab'] = next_bab
    context['prev_bab'] = prev_bab
    context['urutan_bab'] = urutan_bab
    context['urutan_pelajaran'] = urutan_pelajaran
    context['current_bab'] = current_bab
    context['current_pelajaran'] = current_pelajaran
    context['soal'] = Soal.objects.filter(lesson=current_pelajaran).order_by("?").first()
    context['forbidden'] = False
    context['halaman'] = 'pelajaran'

    return context

def enroll(request, slug):
    module = Module.objects.get(slug=slug)
    pelajaran = Pelajaran.objects.filter(module=module).order_by("urutan")
    bab = Bab.objects.filter(module=module).order_by("urutan")

    enroll = Enroll.objects.filter(user=request.user, module=module)

    enroll.update(enroll=True, user=request.user, module=module, bab_module=bab.first(), pelajaran=pelajaran.filter(bab_module=bab.first()).first())
    for i in pelajaran:
        UserPelajaran.objects.create(enroll=enroll.first(), user=request.user, module=module, pelajaran=i, bab_module=i.bab_module)
    for i in bab:
        UserBab.objects.create(enroll=enroll.first(), user=request.user, module=module, bab_module=i)
    
    return module
