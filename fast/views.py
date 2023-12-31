from django.shortcuts import redirect, render
from akun.models import Users
from modul.models.modul import Pelajaran
from modul.models.user import Enroll

def index(request):
    context = {
        'user':Users.objects.filter(teacher=False).count(),
        'teacher':Users.objects.filter(teacher=True).count(),
        'module':Pelajaran.objects.all().count()
    }
    return render(request, 'index.html', context)

def home(request):
    context = {}
    context['enroll'] = Enroll.objects.filter(user=request.user)
    context['mentor'] = Users.objects.filter(teacher=True)[:5]
    return render(request, 'home/index.html', context)