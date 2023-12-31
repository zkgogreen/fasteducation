from django.db import models
from django.contrib.auth.models import User as user_root
Language = [('EN', 'English'),('JP', 'Japan'),('SA', 'Arab'),('CN', 'China')]


class Enroll(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_course_user")
    module       = models.ForeignKey("modul.Module",blank=True, null=True,on_delete=models.CASCADE, related_name="user_module")
    pelajaran   = models.ForeignKey("modul.Pelajaran",blank=True, null=True,on_delete=models.CASCADE, related_name="user_history_pelajaran") #mendapat histori pelajaran
    bab_module   = models.ForeignKey("modul.Bab",blank=True, null=True,on_delete=models.CASCADE, related_name="user_history")                  # mendapat histori bab
    tanggal     = models.DateField(auto_now_add=True)
    finish      = models.BooleanField(default=False)
    like        = models.IntegerField(default=0)
    feed        = models.CharField(blank=True, null=True, max_length=225)
    feedback    = models.CharField(blank=True, null=True, max_length=225)
    enroll      = models.BooleanField(default=False)
    def __str__(self):
        return "{} take {}".format(self.user, self.module)
    def lesson(self):
        return UserPelajaran.objects.filter(enroll=self)
    def percent(self):
        lesson = UserPelajaran.objects.filter(enroll=self)
        bab = UserBab.objects.filter(enroll=self)
        return round(((lesson.filter(isdone=True).count()+bab.filter(isdone=True).count())/(lesson.count()+bab.count()))*100)
    def dipelajari(self):
        return UserPelajaran.objects.filter(enroll=self, isdone=True).count()

# lesson yang sudah dikerjakan
class UserPelajaran(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_lesson_user")
    module       = models.ForeignKey("modul.Module",blank=True, null=True,on_delete=models.CASCADE, related_name="user_module_lesson")
    bab_module   = models.ForeignKey("modul.Bab",blank=True, null=True,on_delete=models.CASCADE, related_name="user_bab_module_lesson")
    pelajaran   = models.ForeignKey("modul.Pelajaran",blank=True, null=True,on_delete=models.CASCADE, related_name="user_pelajaran")
    enroll  = models.ForeignKey(Enroll,blank=True, null=True,on_delete=models.CASCADE, related_name="enroll_lesson")
    isdone      = models.BooleanField(default=False)
    question    = models.CharField(max_length=225, blank=True, null=True)
    answer      = models.CharField(max_length=225, blank=True, null=True)
    tgl         = models.DateField(auto_now_add=False, blank=True, null=True)
    def __str__(self):
        return "{} take {} by {}".format(self.id, self.user, self.pelajaran)
    
    def allow_next(self):
        if self.pelajaran.urutan == 1:
            return True
        return UserPelajaran.objects.filter(pelajaran__urutan=int(self.pelajaran.urutan - 1), isdone=True, bab_module=self.bab_module, user=self.user ).exists()

    
class UserBab(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_bab_user")
    module       = models.ForeignKey("modul.Module",blank=True, null=True,on_delete=models.CASCADE, related_name="user_module_bab")
    bab_module   = models.ForeignKey("modul.Bab",blank=True, null=True,on_delete=models.CASCADE, related_name="userbab_bab")
    enroll      = models.ForeignKey(Enroll,blank=True, null=True,on_delete=models.CASCADE, related_name="enroll_bab")
    isdone      = models.BooleanField(default=False)
    tgl         = models.DateField(auto_now_add=False, blank=True, null=True)
    def __str__(self):
        return "{} take {} by {}".format(self.id, self.user, self.bab_module)
    
    def pelajaran(self):
        return UserPelajaran.objects.filter(bab_module = self.bab_module)
    
    def allow_next(self):
        if self.bab_module.urutan == 1:
            return True
        return UserBab.objects.filter(bab__urutan=int(self.bab.urutan - 1), isdone=True, bab_module=self.bab_module, user=self.user ).exists()


#vocab yang sudah di kerjakan
class UserVocab(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_vocab_user")
    vocab       = models.ForeignKey("modul.VocabGroup", blank=True, null=True,on_delete=models.CASCADE, related_name="vocab")
    level       = models.IntegerField(default=0)
    benar       = models.IntegerField(default=0)
    salah       = models.IntegerField(default=0)
    isdone      = models.BooleanField(default=False)
    def __str__(self):
        return "{}-{}".format(self.user, self.vocab)
    
#games yang sudah di selesaikan
class UserGames(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_games_user")
    games       = models.ForeignKey("modul.Games",blank=True, null=True,on_delete=models.CASCADE, related_name="Usergames_Games")
    module       = models.ForeignKey("modul.Module",blank=True, null=True,on_delete=models.CASCADE, related_name="Usergames_module")
    bab_module   = models.ForeignKey("modul.Bab",blank=True, null=True,on_delete=models.CASCADE, related_name="userbab_games")
    right       = models.IntegerField(default=0) #jumlah benar
    wrong       = models.IntegerField(default=0)  #jumlah salah
    failed      = models.IntegerField(default=0) #jumlah orang yg skip
    def __str__(self):
        return "{} {}{}".format(self.id, self.user, self.games)
    
class UserLatihan(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_latihan_user")
    module       = models.ForeignKey("modul.Module",blank=True, null=True,on_delete=models.CASCADE, related_name="user_module_latihan")
    pelajaran   = models.ForeignKey("modul.Pelajaran",blank=True, null=True,on_delete=models.CASCADE, related_name="user_latihan_pelajaran")
    bab_module   = models.ForeignKey("modul.Bab",blank=True, null=True,on_delete=models.CASCADE, related_name="user_latihan")
    is_last     = models.BooleanField(default=False)
    is_finish   = models.BooleanField(default=False)
    nilai       = models.IntegerField(blank=True, null=True)
    tanggal     = models.DateTimeField(auto_now_add=True)
    countdown   = models.TimeField(default="00:10:00")
    countdownNow= models.TimeField(default="00:10:00")
    def __str__(self):
        return "{}{}".format(self.user, self.nilai)

    def soal(self):
        return UserQuestion.objects.filter(latihan=self)
    

class UserQuestion(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_question_user")
    questions   = models.ForeignKey("modul.Soal",blank=True, null=True,on_delete=models.CASCADE, related_name="UserQuestion_Question")
    module       = models.ForeignKey("modul.Module",blank=True, null=True,on_delete=models.CASCADE, related_name="UserQuestion_module")
    bab_module   = models.ForeignKey("modul.Bab",blank=True, null=True,on_delete=models.CASCADE, related_name="userbab_Question")
    latihan     = models.ForeignKey(UserLatihan,blank=True, null=True,on_delete=models.CASCADE, related_name="user_latihan")
    selected    = models.CharField(max_length=225, blank=True, null=True)
    right       = models.BooleanField(default=False)
    tanggal     = models.DateField(auto_now_add=True)
    def __str__(self):
        return "{} {}{}".format(self.id, self.user, self.questions)
    