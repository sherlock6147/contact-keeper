from django.db import models
from django.utils import timezone

# Create your models here.

class Event(models.Model):
    name = models.CharField("Event Name",max_length=150)
    start_date = models.DateField("start date")
    end_date = models.DateField("end date")
    current = models.BooleanField("Current Event",default=False)
    def __str__(self):
        return self.name

class Website(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    url = models.CharField("Link for website",max_length=250)
    name = models.CharField("Name for website",max_length=250)
    web_cache = models.CharField("Cache of website content",max_length=100000,default='')
    last_visit = models.DateTimeField("last visited on",auto_now=True)
    created_on = models.DateTimeField("Created on",auto_created=True,default=timezone.now)
    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField("Name",max_length=150)
    last_save = models.DateTimeField("Last saved on",auto_now=True)

class PhoneNumber(models.Model):
    phoneNumber = models.CharField("Phone No.",max_length=20)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

class Email(models.Model):
    email = models.CharField("Email",max_length=100)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)