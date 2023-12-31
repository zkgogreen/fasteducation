from django.contrib import admin

# Register your models here.
from config.models import Setting, QnA, Master, Level, Kategori, Advance

admin.site.register(Setting)
admin.site.register(QnA)
admin.site.register(Master)
admin.site.register(Level)
admin.site.register(Kategori)
admin.site.register(Advance)