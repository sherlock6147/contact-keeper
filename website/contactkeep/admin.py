from django.contrib import admin
from .models import Website,Contact,PhoneNumber,Email,Event
# Register your models here.

admin.site.register(Website)
admin.site.register(Contact)
admin.site.register(PhoneNumber)
admin.site.register(Email)
admin.site.register(Event)