from django.shortcuts import render, redirect
from akun.models import Users
from kelas.models import Program, UserMeeting, UserSchadule, Kelas, Schadule, Langganan
from akun.models import UserMentor
from transaksi.models import Transaksi
from transaksi.utils import purchase, midtrans

from kelas.utils import upgradeKelas, confirmUpgrade, upgradeAkun
from transaksi.utils import status
from django.contrib import messages

import datetime
x = datetime.datetime.now()

context = {}
# Create your views here.
def index(request):
    transaksi               = Transaksi.objects.filter(user=request.user, terbayar=True)
    meeting                 = UserMeeting.objects.filter(transaksi=transaksi.filter(terpakai=True).first(), mentor__isnull=False)
    room                    = UserSchadule.objects.filter(user=request.user)
    if not transaksi.exists():
        return redirect("kelas:upgrade")
    if not transaksi.filter(terpakai=True).exists():
        return redirect("kelas:jadwal")
    
    if request.method == 'POST':
        sch =  Schadule.objects.filter(program=meeting.first().program, time=request.POST["time"], tanggal=request.POST["date"]).order_by("?")
        if sch.exists():
            sch_first = sch.first()
            room.filter(id=request.POST['id']).update(schadule=sch_first, room=sch_first.room, tanggal=sch_first.tanggal)
            messages.success(request, 'Anda akan belajar dengan {} pada tangal {} jam {}'.format(sch_first.mentor.first_name+" "+sch_first.mentor.last_name, sch_first.tanggal, sch_first.get_time_display()))
            return redirect("kelas:index")
        else:
            messages.error(request, 'Kelas tidak ditemukan, coba ganti tanggal lain atau jam lain')
            return redirect("kelas:index")
        
    context["user"]         = Users.objects.get(user=request.user)
    context['yet']          = room.filter(hadir=False, tanggal__gte=x).order_by("tanggal")[:5]
    context['done']         = room.filter(tanggal__lt=x)[:5]
    context['meeting']      = meeting.first()
    return render(request, "kelas/index.html", context)

def upgrade(request):
    context["user"]     = Users.objects.get(user=request.user)
    context['paket'] = Program.objects.all().order_by("biaya")
    return render(request, "kelas/upgrade.html", context)

def confirm(request,id):
    url = upgradeKelas(request, id)
    return redirect(url)

def thank(request):
    id = request.GET.get('order_id')
    trans = status(id)
    if request.GET.get('transaction_status') == "settlement":
        transaksi = Transaksi.objects.get(id=id)
        confirmUpgrade(request, transaksi)
        transaksi.terbayar = True
        transaksi.save()
        return render(request, "kelas/thank.html", context={})
    else:
        UserMeeting.objects.filter(SessionID=trans["Data"]["SessionId"]).delete()
        return redirect('kelas:upgrade')
    
def jadwal(request):
    transaksi                 = Transaksi.objects.filter(user=request.user, terbayar=True, terpakai=False).first()
    meeting = UserMeeting.objects.get(user=request.user, transaksi=transaksi)
    if request.method == 'POST':
        kelas    = Kelas.objects.get(id=request.POST["id"])
        transaksi.terpakai = True
        transaksi.save()
        meeting.kelas    = kelas
        meeting.mentor  = kelas.mentor
        meeting.save()
        UserMentor.objects.create(mentor=kelas.mentor, user=request.user, isMentored=True, start=kelas.mulai, end=(kelas.mulai + datetime.timedelta(days=90)))
        for i in Schadule.objects.filter(room=kelas):
            UserSchadule.objects.create(room=kelas, schadule=i, user=request.user,meeting=meeting, tanggal = i.tanggal)
        return redirect("kelas:index")

    context["user"]         = Users.objects.get(user=request.user)
    context['mentor']       = Kelas.objects.filter(program=transaksi.program)
    context['meeting']      = UserMeeting.objects.get(user=request.user, transaksi=transaksi)
    return render(request, "kelas/jadwal.html", context)

def pertemuan(request):
    context["user"]         = Users.objects.get(user=request.user)
    context['jadwal']       = UserSchadule.objects.filter(user=request.user).order_by("tanggal")
    return render(request, "kelas/pertemuan.html", context)

def premium(request):
    url = upgradeAkun(request, id=request.POST['id'])
    return redirect(url)