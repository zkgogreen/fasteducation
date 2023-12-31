from django.shortcuts import redirect, render
from django.contrib.auth.models import User as user_root
from django.http import JsonResponse
from kelas.models import Program, Langganan
from config.models import Level, Kategori, Master, Setting
from modul.models.modul import Module, Bab, Pelajaran, Soal
from modul.models.user import UserBab, Enroll, UserLatihan, UserPelajaran
from akun.models import Users, Teacher

from transaksi.utils import purchase
from kelas.utils import ambilKelas, buatKelas

import datetime
x = datetime.datetime.now()
import random
from datetime import datetime, timedelta

jam     = [(0,'07:30'),(1,'09:00'),(2,'10:30'),(3,'13:00'),(4,'14:30'),(5,'16:00'),(6,'18:30'),(7,'20:00')]
jadwal = [(0, 'senin,  rabu, jum\'at'),(1, 'selasa,  kamis, sabtu'),(2, 'jum\'at,  sabtu, minggu')]

def random_date(start_date, end_date):
    # Convert input strings to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    date_range = end_date - start_date

    random_days = random.randint(0, date_range.days)
    random_date_result = start_date + timedelta(days=random_days)

    return random_date_result

def begin(request):
    try:
        Program.objects.all().delete()
        Langganan.objects.all().delete()
        Level.objects.all().delete()
        Kategori.objects.all().delete()
        Master.objects.all().delete()
        Setting.objects.all().delete()

        Module.objects.all().delete()
        Bab.objects.all().delete()
        Pelajaran.objects.all().delete()
        Soal.objects.all().delete()

        UserBab.objects.all().delete()
        Enroll.objects.all().delete()
        UserLatihan.objects.all().delete()
        UserPelajaran.objects.all().delete()
        user_root.objects.all().delete()
        Users.objects.all().delete()
        Teacher.objects.all().delete()
        user_root.objects.create_superuser(username='jaka', email='inijakaganteng@gmail.com', password='jakaajah')
        
        if not Setting.objects.all().exists():
            Setting.objects.create(title="Mahir SPEAKING di bulan pertama", sub="Kuasai Bahasa Inggris dengan Lebih Cepat: Speaking Sebagai Native Speaker dalam Sebulan Tanpa Hafalan!", icon="landing/icon.png", logo="landing/icon.png", foto="landing/jumbotron.png")

        langganan1 = Langganan.objects.create(durasi=1, harga=30000, diskon=30000)
        langganan2 = Langganan.objects.create(durasi=3, harga=50000, diskon=50000)
        langganan3 = Langganan.objects.create(durasi=6, harga=80000, diskon=80000)
        langganan4 = Langganan.objects.create(durasi=12, harga=100000, diskon=100000)

        Program1  = Program.objects.create(langganan=langganan2, foto="level/free.png",siswa=50,pertemuan=30, nama='free', keterangan='belajar bahasa inggris tidak butuh biaya',  nyawa=5, biaya=10000, discount=10000,promo=0,materi="GRAMMAR FOR SPEAKING, PRONUNCIATION, VOCABULARY, SPEAKING PRACTICE", bonus="Garansi mengulang, Free 60x Written Class, Free 10x Pronunciation Class, Gratis konsultasi langsung dengan tutor", ketentuan="Microphone wajib aktif ketika sesi praktek, Biaya tidak hangus jika tidak hadir, Bebas pilih jadwal atau merubah jadwal, Dilarang keras membahas isu politik atau SARA ketika praktek"),
        Program2  = Program.objects.create(langganan=langganan2, foto="level/private.png",siswa=30,pertemuan=30, nama='membersip', keterangan='belajar bahasa inggris dengan intensif',  nyawa=100, biaya=80000,discount=80000,promo=0,materi="GRAMMAR FOR SPEAKING, PRONUNCIATION, VOCABULARY, SPEAKING PRACTICE", bonus="Garansi mengulang, Free 60x Written Class, Free 10x Pronunciation Class, Gratis konsultasi langsung dengan tutor", ketentuan="Microphone wajib aktif ketika sesi praktek, Biaya tidak hangus jika tidak hadir, Bebas pilih jadwal atau merubah jadwal, Dilarang keras membahas isu politik atau SARA ketika praktek")
        Program3  = Program.objects.create(langganan=langganan2, foto="level/premium.png",siswa=10,pertemuan=30, nama='Premium', keterangan='belajar bahasa inggris tanpa batasan', nyawa=100, biaya=120000,discount=120000,promo=0,materi="GRAMMAR FOR SPEAKING, PRONUNCIATION, VOCABULARY, SPEAKING PRACTICE", bonus="Garansi mengulang, Free 60x Written Class, Free 10x Pronunciation Class, Gratis konsultasi langsung dengan tutor", ketentuan="Microphone wajib aktif ketika sesi praktek, Biaya tidak hangus jika tidak hadir, Bebas pilih jadwal atau merubah jadwal, Dilarang keras membahas isu politik atau SARA ketika praktek")
        Program4  = Program.objects.create(langganan=langganan2, foto="level/private.png",siswa=1,pertemuan=30, nama='Private', keterangan='belajar bahasa inggris tanpa batasan', nyawa=100, biaya=240000,discount=240000,promo=0,materi="GRAMMAR FOR SPEAKING, PRONUNCIATION, VOCABULARY, SPEAKING PRACTICE", bonus="Garansi mengulang, Free 60x Written Class, Free 10x Pronunciation Class, Gratis konsultasi langsung dengan tutor", ketentuan="Microphone wajib aktif ketika sesi praktek, Biaya tidak hangus jika tidak hadir, Bebas pilih jadwal atau merubah jadwal, Dilarang keras membahas isu politik atau SARA ketika praktek")
        Program5  = Program.objects.create(langganan=langganan2, foto="level/foregn.png",siswa=1,pertemuan=30, nama='Private with foregn', keterangan='belajar bahasa inggris tanpa batasan', nyawa=100, biaya=500000,discount=500000,promo=0,materi="GRAMMAR FOR SPEAKING, PRONUNCIATION, VOCABULARY, SPEAKING PRACTICE", bonus="Garansi mengulang, Free 60x Written Class, Free 10x Pronunciation Class, Gratis konsultasi langsung dengan tutor", ketentuan="Microphone wajib aktif ketika sesi praktek, Biaya tidak hangus jika tidak hadir, Bebas pilih jadwal atau merubah jadwal, Dilarang keras membahas isu politik atau SARA ketika praktek")
        
        Program_list = [Program1, Program2, Program3, Program4, Program5]

        level1      = Level.objects.create(name="Beginner", keterangan="kemampuan bahasa Inggris yang masih sangat dasar.")
        level2      = Level.objects.create(name="Elementary", keterangan="dapat berkomunikasi dengan bahasa Inggris, tetapi pembahasan hanya mencakup hal-hal tertentu yang telah dikuasai.")
        level3      = Level.objects.create(name="Intermediate", keterangan="berbahasa Inggris secara pasif dan aktif dengan topik yang lebih variatif.")
        level4      = Level.objects.create(name="Advanced", keterangan="menggunakan bahasa Inggris untuk kepentingan akademis dan profesional.")
        level5      = Level.objects.create(name="Expert", keterangan="setara dengan native speaker (penutur asli)")
        level_list = [level1, level2, level3, level4, level5]
        
        #kategori
        kategori1   = Kategori.objects.create(name="Speaking", keterangan="Kemampuan Berbicara ")
        kategori2   = Kategori.objects.create(name="Reading", keterangan="Kemampuan Membaca")
        kategori3   = Kategori.objects.create(name="Listening", keterangan="Keterampilan Menyimak")
        kategori4   = Kategori.objects.create(name="Writing", keterangan="Kemampuan Menulis")
        kategori5   = Kategori.objects.create(name="Pronunciation", keterangan="Kemampuan Pengucapan")
        kategori6   = Kategori.objects.create(name="Vocabulary ", keterangan="Kemampuan Kosakata")
        kategori_list = [kategori1, kategori2, kategori3, kategori4, kategori5, kategori6]

        #master
        master1     = Master.objects.create(name="TOEFL", keterangan="Test of English as Foregn Language")
        master2     = Master.objects.create(name="Public Speaking", keterangan="Keterampilan berbicara dengan banyak orang")
        mater_list = [master1, master2]
        

        for k in range(1,4):
            module = Module.objects.create(nama="module ke-"+str(k), bahasa=1, slug="moduleKe-"+str(k), photo=f'module/banner{k}.jpg', kategori=kategori1, level=level1,keterangan="keterangan", rangkuman="rangkuman", urutan=k)
            for i in range(1,6):
                bab = Bab.objects.create(module=module, bab="module {} Bab {}".format(k, i), urutan=i, rangkuman="ini adalah rangkuman")
                for j in range(1,6):
                    pelajaran = Pelajaran.objects.create(module=module, urutan=j, bab_module=bab, judul="module {} Bab {} judul {}".format(k,i, j), keterangan="ini adalah keterangan "+str(j), text="ini adalah text "+str(j), approve=True)
                    for k in range(1,4):
                        Soal.objects.create(category=kategori1, level=level1, module=module, bab_module=bab, lesson=pelajaran, soal="module {} Bab {} judul {} question {}".format(k,i, j, k), answer="benar", wrong1="salah 1", wrong2="salah 2", wrong3="salah 3", penjelasan="Penjelasan {} Bab {} judul {} question {}".format(k,i, j, k), approve=True)

        user_list = []
        user_obj_list = []
        for u in range(40):
            user = user_root.objects.create_user(username="user_"+str(u), email="user_{}@localhost".format(u), first_name="user", last_name="ke-"+str(u), password="user1234")
            user_obj = Users.objects.create(user=user)
            user_list.append(user)
            user_obj_list.append(user_obj)
        
        mentor_list = []
        mentor_obj_list = []
        for u in range(5):
            mentor = user_root.objects.create_user(username="mentor_"+str(u), email="mentor_{}@localhost".format(u), first_name="mentor", last_name="ke-"+str(u), password="mentor1234")
            mentor_obj = Users.objects.create(user=mentor, teacher=True)
            mentor_list.append(mentor)
            mentor_obj_list.append(mentor_obj)
            Teacher.objects.create(user=mentor, mastered=mater_list[random.randint(0,1)])

        kelas_list = []
        for m in mentor_list:
            for c in range(random.randint(1,5)):
                kelas = buatKelas(user=m,program=Program_list[random.randint(1,4)], jam=random.randint(0,7), jadwal=random.randint(0,2), mulai=random_date("2023-01-01", "2023-12-29").strftime("%Y-%m-%d"))
                kelas_list.append(kelas)

        user_purchased = []
        for u in user_list:
            rand = random.randint(1,4)
            transaksi = purchase(user=u, program=Program_list[rand])
            user_purchased.append(transaksi)

        for tramsaksi in user_purchased:
            rand = random.randint(0,len(kelas_list)-1)
            ambilKelas(tramsaksi, kelas=kelas_list[rand])
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': e}) 