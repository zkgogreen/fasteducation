from django.db import models
from django.contrib.auth.models import User as user_root
from config.models import Level
from akun.models import Users, Teacher

# Create your models here.
Language = [('EN', 'English'),('JP', 'Japan'),('SA', 'Arab'),('CN', 'China')]
jam     = [(0,'07:30'),(1,'09:00'),(2,'10:30'),(3,'13:00'),(4,'14:30'),(5,'16:00'),(6,'18:30'),(7,'20:00')]
jadwal = [(0, 'senin,  rabu, jum\'at'),(1, 'selasa,  kamis, sabtu'),(2, 'jum\'at,  sabtu, minggu')]

class Langganan(models.Model):
    durasi      = models.IntegerField(default=1)
    harga       = models.IntegerField(default=50000)
    diskon      = models.IntegerField(default=40000)
    def __str__(self):
        return "{} by {}".format(self.durasi, self.diskon)
    
class Program(models.Model):
    nama        = models.CharField(max_length=224,  unique=True)
    foto        = models.FileField(upload_to='photo/level', max_length=100, null=True, blank=True)
    keterangan  = models.CharField(max_length=224)
    nyawa       = models.IntegerField(default=0)
    biaya       = models.IntegerField(default=0)
    discount    = models.IntegerField(default=0)
    promo       = models.IntegerField(default=0)
    bestseller  = models.BooleanField(default=False)
    pertemuan   = models.IntegerField(default=0)
    siswa       = models.IntegerField(default=0)
    durasi      = models.IntegerField(default=1)
    mengulang   = models.BooleanField(default=False)
    ketentuan   = models.CharField(max_length=225, blank=True, null=True)
    materi      = models.CharField(max_length=225, blank=True, null=True)
    bonus       = models.CharField(max_length=225, blank=True, null=True)
    langganan   = models.ForeignKey(Langganan,blank=True, null=True,  on_delete=models.CASCADE, related_name="langganan")
    def __str__(self):
        return "{}".format(self.nama)
    
    def ketentuans(self):
        return self.ketentuan.split(",")
    def materis(self):
        return self.materi.split(",")
    def bonuses(self):
        return self.bonus.split(",")
    
class Kelas(models.Model):
    mentor      = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE,related_name="teacher_room")
    bahasa      = models.CharField(choices=Language, blank=True, max_length=3, default=1)
    program     = models.ForeignKey(Program,blank=True, null=True,on_delete=models.CASCADE, related_name="program_akun_room")
    level       = models.ForeignKey(Level,blank=True, null=True,on_delete=models.CASCADE, related_name="level_akun_room")
    time        = models.IntegerField(choices=jam, blank=True, default=1)
    mulai       = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    jadwal      = models.IntegerField(choices=jadwal, blank=True, default=1)
    def __str__(self):
        return "{} {}".format(self.mentor, self.jadwal)
    def user(self):
        return Users.objects.get(user=self.mentor)
    def teacher(self):
        return Teacher.objects.get(user=self.mentor)
    def peserta(self):
        return UserMeeting.objects.filter(kelas=self).count()
        

class Schadule(models.Model):
    room        = models.ForeignKey(Kelas,blank=True, null=True,on_delete=models.CASCADE, related_name="teacher_schadule_room")
    mentor      = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE,related_name="mentor_schadule")
    terlaksana  = models.BooleanField(default=False)
    time        = models.IntegerField(choices=jam, blank=True, default=1)
    program     = models.ForeignKey(Program,blank=True, null=True,on_delete=models.CASCADE, related_name="level_akun_schadule")
    tanggal     = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    def __str__(self):
        return "{} {}".format(self.room, self.tanggal)
    
class UserMeeting(models.Model):
    mentor      = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="mentor_meeting")
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_meeting")
    kelas       = models.ForeignKey(Kelas, blank=True, null=True,on_delete=models.CASCADE, related_name="user_meeting")
    program     = models.ForeignKey(Program, blank=True, null=True,on_delete=models.CASCADE, related_name="user_meeting")
    transaksi   = models.ForeignKey('transaksi.Transaksi', blank=True, null=True,on_delete=models.CASCADE, related_name="user_transaksi")
    start       = models.DateField(auto_now_add=True)
    end         = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    meetremain  = models.IntegerField(default=0)
    def __str__(self):
        return "{}. {}-{}".format(self.id, self.user, self.meetremain)

    
#user yang mendaftar
class UserSchadule(models.Model):
    room        = models.ForeignKey(Kelas,blank=True, null=True,on_delete=models.CASCADE, related_name="room_room")
    schadule    = models.ForeignKey(Schadule,blank=True, null=True,on_delete=models.CASCADE, related_name="room_schadule")
    user        = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE,related_name="user_room")
    meeting     = models.ForeignKey(UserMeeting,blank=True, null=True,on_delete=models.CASCADE,related_name="user_meeting")
    hadir       = models.BooleanField(default=False)
    feedback    = models.CharField(max_length=225, blank=True, null=True)
    performance = models.IntegerField(blank=True, null=True)
    tanggal     = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    def __str__(self):
        return "{} {}".format(self.room, self.tanggal)
    