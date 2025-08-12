from django.contrib import admin
from hospitalapp.models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Ward)
admin.site.register(Appoint)
admin.site.register(Contact)
admin.site.register(Transaction)
