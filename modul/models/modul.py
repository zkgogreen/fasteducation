from django.db import models
from django.contrib.auth.models import User as user_root
from ckeditor.fields import RichTextField
from config.models import Level, Kategori
from modul.models.user import Enroll, UserPelajaran
from django.db.models import Avg
import random

Language = [('EN', 'English'),('JP', 'Japan'),('SA', 'Arab'),('CN', 'China')]
# Create your models here.
class Module(models.Model):
    nama        = models.CharField(max_length=224)
    bahasa      = models.CharField(max_length=3,choices=Language, blank=True)
    slug        = models.SlugField(max_length=30, null=True)
    photo       = models.FileField(upload_to='module', max_length=100, default="module/default.jpg")
    kategori    = models.ForeignKey(Kategori,blank=True, null=True,on_delete=models.CASCADE, related_name="kategori_module")
    level       = models.ForeignKey(Level,blank=True, null=True,on_delete=models.CASCADE, related_name="level_module")
    keterangan  = models.CharField(blank=True,max_length=224)
    rangkuman   = RichTextField(blank=True, null=True)
    defaultget  = models.BooleanField(default=False)
    biaya       = models.IntegerField(default=0)
    discount    = models.IntegerField(default=0)
    premium     = models.BooleanField(default=False)
    mahkota     = models.IntegerField(default=0)
    dilihat     = models.IntegerField(default=0)
    certificate = models.BooleanField(default=False)
    rilis       = models.BooleanField(default=False)
    urutan      = models.IntegerField(blank=True, null=True)

    enroll      = Enroll.objects.all()
    def __str__(self):
        return " {}".format(self.nama)
    def subscribe(self):
        return self.enroll.filter(module=self, enroll=True).count()
    def pelajaran(self):
        return Pelajaran.objects.filter(module=self).count()
    def finish(self):
        return self.enroll.filter(module=self, finish=True).count()
    def bab(self):
        return Bab.objects.filter(module=self).count()
    def see(self):
        return self.enroll.filter(module=self).count()
    def feedback(self):
        return self.enroll.filter(module=self, feedback__isnull=False).count()
    def ratting(self):
        return self.enroll.filter(module=self).aggregate(Avg('like'))['like__avg']
    
    def getBab(self):
        return Bab.objects.filter(module=self).order_by('urutan')
    
    def is_subscribe(self, user):
        return Enroll.objects.filter(module=self, user=user)
    
# perubahan module yang ajukan oleh guru
class Update(models.Model):
    user        = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE, related_name="user_creator")
    module       = models.ForeignKey(Module,blank=True, null=True,on_delete=models.CASCADE, related_name="module_creator")
    perubahan   = models.CharField(max_length=225)
    approve     = models.BooleanField(default=False)
    date        = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{}-{}".format(self.user, self.module)
    
# bab pada lesson
class Bab(models.Model):
    module       = models.ForeignKey(Module,blank=True, null=True,on_delete=models.CASCADE, related_name="module_bab")
    bab         = models.CharField(max_length=50)
    urutan      = models.IntegerField(blank=True, null=True)
    rangkuman   = RichTextField(blank=True, null=True)
    premium     = models.BooleanField(default=False)
    def __str__(self):
        return "{}-{}".format(self.module, self.bab)
    def getPelajaran(self):
        return Pelajaran.objects.filter(bab_module=self).order_by("urutan")
    

class Pelajaran(models.Model):
    module       = models.ForeignKey(Module,blank=True, null=True,on_delete=models.CASCADE, related_name="module_pelajaran")
    urutan      = models.IntegerField(blank=True, null=True)
    bab_module   = models.ForeignKey(Bab,blank=True, null=True,on_delete=models.CASCADE, related_name="bab_module")
    judul       = models.CharField(max_length=224)
    keterangan  = models.CharField(max_length=224, default="belum ada keterangan")
    vidio       = models.URLField(max_length=200, null=True, blank=True)
    text        = RichTextField()
    date        = models.DateField(auto_now_add=True, blank=True)
    approve     = models.BooleanField(default=False)
    def __str__(self):
        return "{}-{}".format(self.id, self.judul)
    
    def isdone(self, request):
        return UserPelajaran.objects.filter(user=request.user, pelajaran=self).exists()


class Soal(models.Model):
    category    = models.ForeignKey(Kategori,blank=True, null=True,on_delete=models.CASCADE, related_name="quest_kategori")
    level       = models.ForeignKey(Level,blank=True, null=True,on_delete=models.CASCADE, related_name="quest_level")
    module       = models.ForeignKey(Module,blank=True, null=True,on_delete=models.CASCADE, related_name="quest_module")
    bab_module   = models.ForeignKey(Bab,blank=True, null=True,on_delete=models.CASCADE, related_name="bab_question")
    lesson      = models.ForeignKey(Pelajaran,blank=True, null=True,on_delete=models.CASCADE, related_name="quest_pelajaran")
    soal        = models.CharField(max_length=224)
    answer      = models.CharField(max_length=224)
    wrong1      = models.CharField(max_length=224)
    wrong2      = models.CharField(max_length=224)
    wrong3      = models.CharField(max_length=224)
    penjelasan  = models.TextField(default="Belum ada penjelasan")
    user        = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE, related_name="user_question")
    approve     = models.BooleanField(default=False)
    def __str__(self):
        return "{}.{}".format(self.soal, self.lesson)
    
    def questionList(self):
        choices = [self.answer, self.wrong1, self.wrong2, self.wrong3]
        random.shuffle(choices)
        return choices
    
class Games(models.Model):
    level       = models.IntegerField()
    soal        = models.CharField(max_length=224)
    answer      = models.CharField(max_length=224)
    dummy       = models.CharField(max_length=224)
    penjelasan  = models.TextField(default="Belum ada penjelasan")
    pelajaran   = models.ForeignKey(Pelajaran,blank=True, null=True,on_delete=models.CASCADE, related_name="games_pelajaran")
    module       = models.ForeignKey(Module,blank=True, null=True,on_delete=models.CASCADE, related_name="Games_module")
    bab_module   = models.ForeignKey(Bab,blank=True, null=True,on_delete=models.CASCADE, related_name="bab_games")
    user        = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE, related_name="user_games")
    approve     = models.BooleanField(default=False)
    def __str__(self):
        return "level {} - {}".format(self.level, self.soal)
    
class VocabGroup(models.Model):
    bahasa      = models.CharField(max_length=3,choices=Language, blank=True)
    origin      = models.CharField(max_length=50)
    translate   = models.CharField(max_length=50)
    level       = models.ForeignKey(Level,blank=True, null=True, on_delete=models.CASCADE, related_name="vocab_group_level")
    img         = models.FileField(upload_to='media/vocabgroup', max_length=100, default="media/vocabgroup/default.jpg")
    def __str__(self):
        return "{}.{}-{}".format(self.id, self.english, self.indo)

#penjabaran dari vocab grup seperti buah = anggur, jeruk dll
class Vocab(models.Model):
    vocabgroup  = models.ForeignKey(VocabGroup,blank=True, null=True, on_delete=models.CASCADE, related_name="vocab_group")
    origin      = models.CharField(max_length=50)
    translate   = models.CharField(max_length=50)
    success     = models.IntegerField(default=0)
    failed      = models.IntegerField(default=0)
    def __str__(self):
        return "{}.{}-{}".format(self.id, self.english, self.indo)