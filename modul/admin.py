from django.contrib import admin
from modul.models.user import Enroll, UserPelajaran, UserBab, UserVocab, UserGames, UserLatihan, UserQuestion
from modul.models.modul import Module, Update, Bab, Pelajaran, Games, VocabGroup, Vocab, Soal
# Register your models here.

admin.site.register(Enroll)
admin.site.register(UserPelajaran)
admin.site.register(UserBab)
admin.site.register(UserVocab)
admin.site.register(UserGames)
admin.site.register(UserLatihan)
admin.site.register(UserQuestion)


admin.site.register(Module)
admin.site.register(Update)
admin.site.register(Bab)
admin.site.register(Pelajaran)
admin.site.register(Soal)
admin.site.register(Games)
admin.site.register(VocabGroup)
admin.site.register(Vocab)