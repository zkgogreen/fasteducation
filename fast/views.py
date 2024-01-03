from django.shortcuts import redirect, render
from akun.models import Users
from modul.models.modul import Pelajaran
from modul.models.user import Enroll
from kelas.models import UserMeeting, UserSchadule

def index(request):
    context = {
        'user':Users.objects.filter(teacher=False).count(),
        'teacher':Users.objects.filter(teacher=True).count(),
        'module':Pelajaran.objects.all().count()
    }
    return render(request, 'index.html', context)

def home(request):
    user = Users.objects.get(user=request.user)
    if user.teacher:
        return teacher_view(request)
    else:
        return user_view(request)


def user_view(request):
    context = {}
    context['kelas'] = UserMeeting.objects.filter(user=request.user).exclude(meetremain=0).first()
    context['enroll'] = Enroll.objects.filter(user=request.user)
    context['mentor'] = Users.objects.filter(teacher=True)[:5]
    context['events'] = UserSchadule.objects.filter(user=request.user)
    return render(request, 'home/index.html', context)

def teacher_view(request):
    context = {}
    return render(request, 'home/teacher.html', context)