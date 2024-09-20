from django.contrib import admin
from core.models import LinkedInSession, JobApplication, Application

# Register your models here.
admin.site.register(LinkedInSession)
admin.site.register(JobApplication)
admin.site.register(Application)
