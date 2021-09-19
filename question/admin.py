from django.contrib import admin

from . import models


admin.site.register(models.Question)
admin.site.register(models.Answer)
# admin.site.register(models.User_Profile)
admin.site.register(models.Sub_question)
admin.site.register(models.category)
admin.site.register(models.User_Profile)
admin.site.register(models.fun)
admin.site.register(models.Contacts)