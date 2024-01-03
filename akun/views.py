from django.shortcuts import render, redirect
from akun.models import Users
from kelas.models import Kelas, UserMeeting
from kelas.utils import joinKelas
from django.contrib import messages

# Create your views here.
def index(request):
    pass

def profile(request, id):
    user = Users.objects.get(id=id)
    root_user = user.user

    otherUser = UserMeeting.objects.filter(user=request.user, mentor__isnull=True)
    
    if request.method == 'POST':
        kls = Kelas.objects.get(id=request.POST['id'])
        try:
            joinKelas(request, kls)
            messages.success(request, f'Kamu berhasil langganan ke kelas {kls.program.nama} bersama {root_user.first_name} {root_user.last_name} pada tanggal {kls.mulai}')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Gagal langganan ke kelas {kls.program.nama}  <br> Error : {e}')
            return redirect("akun:profile", id=id)

    context = {
        'profile': user,
        'kelas':Kelas.objects.filter(mentor=root_user, program=otherUser.first().program) if otherUser.exists() else Kelas.objects.filter(mentor=root_user),
        'otherUser':otherUser.first()
    }
    return render(request, 'user/profile.html', context)