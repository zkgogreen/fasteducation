from django.contrib import admin

from website.models import Artikel, Report, Ask, Event, UserEvent, Improve

admin.site.register(Artikel)
admin.site.register(Report)
admin.site.register(Ask)
admin.site.register(Event)
admin.site.register(UserEvent)
admin.site.register(Improve)