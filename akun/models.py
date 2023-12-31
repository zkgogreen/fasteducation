from django.db import models
from django.contrib.auth.models import User as user_root
from config.models import Level, Master
from django.db.models import Avg

getstatus = ((1, 'user'),(2, 'teacher'),(3, 'owner'))


class Users(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True ,on_delete=models.CASCADE, related_name="user_user")
    birth       = models.DateField(null=True, blank=True)
    address     = models.CharField(max_length=224, blank=True)
    photo       = models.FileField(upload_to='photo/profile', blank=True, null=True)
    join        = models.DateField(auto_now_add=True)                           # kapan join 
    kelas       = models.IntegerField(default=1)
    testi       = models.TextField(blank=True)
    phone       = models.CharField(max_length=224, blank=True)
    promo       = models.BooleanField(default=False)
    teacher     = models.BooleanField(default=False)
    # progress
    xp          = models.IntegerField(default=0)
    nyawa       = models.IntegerField(default=0)
    game        = models.IntegerField(default=0)
    mahkota     = models.IntegerField(default=0)
    level       = models.ForeignKey(Level,to_field='name', default='Beginner',on_delete=models.CASCADE, related_name="progress_user")
    def __str__(self):
        return "{} {}".format(self.id, self.user.username)
    
    def save(self, *args, **kwargs):
        try:
            this = Users.objects.get(id=self.id)
            if this.photo != self.photo:
                this.photo.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)

    def Userteacher(self):
        return Teacher.objects.get(user=self.user)


class Premium(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True ,on_delete=models.CASCADE, related_name="premium_user")
    premium_start= models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)          # akun premium
    premium_end= models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)          # akun premium
    def __str__(self):
        return "{} {}".format(self.user, self.premium_start)

class Teacher(models.Model):
    user        = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE, related_name="user_of_teacher")
    link        = models.CharField(max_length=50, null=True, default="https://zoom.us/")
    password    = models.CharField(max_length=50, null=True, blank=True)
    credits     = models.IntegerField(default=0)
    api_key     = models.CharField(max_length=50, null=True)
    secret_key  = models.CharField(max_length=50, null=True)
    mastered    = models.ForeignKey(Master,blank=True, null=True,on_delete=models.CASCADE, related_name="Master_of_teacher")
    desc        = models.CharField(max_length=225, null=True)
    pendapatan  = models.IntegerField(default=0)
    def __str__(self):
        return " {}".format(self.user)
    
    def ratting(self):
        return UserMentor.objects.filter(mentor=self.user).aggregate(Avg('like'))['like__avg']

#jika sudah di mentor langsung 
class UserMentor(models.Model):
    mentor      = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE,related_name="user_teacher")
    user        = models.ForeignKey(user_root,blank=True, null=True,on_delete=models.CASCADE,related_name="user_mentor")
    isMentored  = models.BooleanField(default=False)
    start       = models.DateField(auto_now=False, auto_now_add=False)
    end         = models.DateField(auto_now=False, auto_now_add=False)
    like        = models.IntegerField(blank=True, null=True)
    message     = models.CharField(max_length=224, blank=True)
    def __str__(self):
        return "{} - {}.{}".format(self.user, self.mentor, self.like)