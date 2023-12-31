from django.db import models
from django.contrib.auth.models import User as user_root

# Create your models here.
class Artikel(models.Model):
    arrjenis    = ( (0,'news'),(1,'tips'))
    slug        = models.CharField(max_length=224)
    title       = models.CharField(max_length=224)
    header      = models.CharField(max_length=224, default="this is header text of content")
    foto        = models.FileField(upload_to='article', blank=True)
    jenis       = models.IntegerField(choices=arrjenis, default=0)
    text        = models.TextField(blank=True)
    tanggal     = models.DateTimeField(auto_now_add=True)
    dibaca      = models.IntegerField(default=0)
    user        = models.ForeignKey(user_root,blank=True, null=True,  on_delete=models.CASCADE, related_name="user_artikel")
    def __str__(self):
        return "{}".format(self.slug)

class Report(models.Model):
    arrReport   = ( (0,'report'),(1,'update'))
    user        = models.ForeignKey(user_root,blank=True, null=True,  on_delete=models.CASCADE, related_name="user_report")
    jenis       = models.IntegerField(default=0, choices=arrReport)
    text        = models.TextField(blank=True)
    tanggal     = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return "{}.{}".format(self.jenis, self.user)
    
class Ask(models.Model):
    nama = models.CharField(max_length=224)
    kontak = models.CharField(max_length=224)
    text = models.TextField(blank=True)
    closed = models.BooleanField(default=False)
    def __str__(self):
        return "{}".format(self.nama)
    
class Event(models.Model):
    Hadiah = (
        (0,'credit'),
        (1,'barang'),
        (2,'kelas'),
        (3,'jabatan')
    )
    slug        = models.CharField(max_length=224, default="this-is-slug")
    photo       = models.FileField(upload_to='event', max_length=100, default="example.jpg")
    nama        = models.CharField(max_length=224)
    hadiah      = models.CharField(max_length=224)
    jenis       = models.IntegerField(choices=Hadiah, default=0)
    by          = models.OneToOneField(user_root,blank=True, null=True,  on_delete=models.CASCADE, related_name="user_event")
    sponsor     = models.CharField(max_length=224)
    peraturan   = models.TextField(blank=True)
    mulai       = models.DateField(blank=True, null=True)
    selesai     = models.DateField(blank=True, null=True)
    def __str__(self):
        return "{} hadiah {}".format(self.nama, self.hadiah)

    def save(self, *args, **kwargs):
        try:
            this = Event.objects.get(id=self.id)
            if this.photo != self.photo:
                this.photo.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)

class UserEvent(models.Model):
    user      = models.OneToOneField(user_root, on_delete=models.CASCADE, related_name="user_event_sender")
    eventname   = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="event")
    file        = models.FileField(upload_to='file/event', max_length=100, null=True, blank=True)
    done        = models.BooleanField(default=False)
    def __str__(self):
        return "{} mengikuti {}".format(self.user, self.eventname)

class Improve(models.Model):
    what        = models.CharField(max_length=224)
    why         = models.CharField(max_length=224)
    how         = models.TextField()
    def __str__(self):
        return "{}".format(self.what)