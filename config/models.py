from django.db import models

# Create your models here.
class Setting(models.Model):
    title       = models.CharField(max_length=224)
    sub         = models.TextField()
    icon        = models.FileField(upload_to='landing', blank=True, )
    logo        = models.FileField(upload_to='landing', blank=True, )
    foto        = models.FileField(upload_to='landing', blank=True, )
    fotoadv     = models.FileField(upload_to='landing', blank=True, )
    alamat      = models.CharField(max_length=224, blank=True, )
    telp        = models.CharField(blank=True,max_length=13 )
    email       = models.EmailField(blank=True, )
    ig          = models.CharField(max_length=224, blank=True, )
    fb          = models.CharField(max_length=224, blank=True, )
    tiktok      = models.CharField(max_length=224, blank=True, )
    youtube     = models.CharField(max_length=224, blank=True, )
    komisi_teacher = models.IntegerField(default=70)
    komisi_developer = models.IntegerField(default=7)
    komisi_owner = models.IntegerField(default=23)
    def __str__(self):
        return "{}".format(self.title)
    def save(self, *args, **kwargs):
        try:
            this = Setting.objects.get(id=self.id)
            if this.icon != self.icon:
                this.icon.delete(save=False)
            if this.logo != self.logo:
                this.logo.delete(save=False)
            if this.foto != self.foto:
                this.foto.delete(save=False)
            if this.fotoadv != self.fotoadv:
                this.fotoadv.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)

class Advance(models.Model):
    icon        = models.CharField(max_length=224)
    nama        = models.CharField(max_length=224)
    ket         = models.CharField(max_length=224)
    def __str__(self):
        return "{}".format(self.nama)
    
class QnA(models.Model):
    quest       = models.CharField(max_length=224)
    answer      = models.CharField(max_length=224)
    klik        = models.IntegerField(default=0)
    def __str__(self):
        return "{} by {}".format(self.quest, self.klik)
    
class Level(models.Model):
    name        = models.CharField(max_length=224,  unique=True)
    keterangan  = models.CharField(max_length=224)
    def __str__(self):
        return "{} by {}".format(self.name, self.keterangan)

class Master(models.Model):
    name        = models.CharField(max_length=224,  unique=True)
    keterangan  = models.CharField(max_length=224)
    def __str__(self):
        return "{} by {}".format(self.name, self.keterangan)

class Kategori(models.Model):
    name        = models.CharField(max_length=224,  unique=True)
    keterangan  = models.CharField(max_length=224)
    def __str__(self):
        return "{} by {}".format(self.name, self.keterangan,  unique=True)