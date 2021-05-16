from datetime import datetime
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, request
from .models import *
from django.utils import timezone
import requests as req,html5lib,bs4
# Create your views here.

def home(request):
    current_event = Event.objects.filter(current=True)
    if current_event.count() != 0:
        current_event = current_event[0]
    else:
        current_event = "no event"
    context = {
        'event' : current_event,
    }
    return render(request,'contactkeep/home.html',context)

def events(request):
    if request.method == 'POST':
        if 'event-add' in request.POST:
            event = Event()
            event.name = request.POST.get('name')
            if request.POST['start_date'] != '':
                event.start_date = request.POST.get('start_date')
            if request.POST['end_date'] != '':
                event.end_date = request.POST.get('end_date')
            if 'current' in request.POST:
                if request.POST['current'] == False:
                    event.current = False
                else:
                    existing_current_event = Event.objects.filter(current=True)
                    if existing_current_event.count() != 0: 
                        existing_current_event = existing_current_event[0]
                        existing_current_event.current = False
                        existing_current_event.save()
                    event.current = True
            else:
                event.current = False
            event.save()
            return HttpResponseRedirect('/events/')
        if 'event-delete' in request.POST:
            id = int(request.POST.get('event_id'))
            event = get_object_or_404(Event,id=id)
            delete_event(request,event)
    all_events = Event.objects.order_by('start_date')
    context = {
        'list_of_events' : all_events,
    }
    return render(request,'contactkeep/events.html',context)

def event_edit(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    if request.method == 'POST':
        if 'event-edit' in request.POST:
            event.name = request.POST.get('name')
            if request.POST['start_date'] != '':
                event.start_date = request.POST.get('start_date')
            if request.POST['end_date'] != '':
                event.end_date = request.POST.get('end_date')
            if 'current' in request.POST:
                if request.POST['current'] == False:
                    event.current = False
                else:
                    existing_current_event = Event.objects.filter(current=True)
                    if existing_current_event.count() != 0: 
                        existing_current_event = existing_current_event[0]
                        existing_current_event.current = False
                        existing_current_event.save()
                    event.current = True
            else:
                event.current = False
            event.save()
            return HttpResponseRedirect('/events/')
    context = {
        'event' : event,
    }
    return render(request,'contactkeep/event_edit.html',context)

def event_details(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    if 'event-delete' in request.POST:
            delete_event(request,event)
    context = {
        'event' : event,
    }
    return render(request,'contactkeep/event_details.html',context)

def delete_event(request,event):
    event.delete()
    print("event deleted")
    return HttpResponseRedirect('/events/')

def websites(request):
    current_event = Event.objects.filter(current=True)
    if(current_event.count()!=0):
        current_event = current_event[0]
        websites_for_event = Website.objects.filter(event=current_event).order_by('-last_visit')
    else:
        websites_for_event = "no event selected"
    if request.method == 'POST':
        if 'website-add' in request.POST:
            website = Website()
            website.name = request.POST.get('name')
            website.url = request.POST.get('url')
            website.event = current_event
            website.save()
            return HttpResponseRedirect('/websites/')
        if 'website-delete' in request.POST:
            website_id = request.POST.get('website_id')
            website = get_object_or_404(Website,id=website_id)
            delete_website(request,website)
    context = {
        'event' : current_event,
        'websites_for_event' : websites_for_event,
    }
    return render(request,'contactkeep/websites.html',context)

def delete_website(request,website):
    website.delete()
    return HttpResponseRedirect('/websites/')

def website_view(request,website_id):
    website = get_object_or_404(Website,id=website_id)
    if 'refresh' in request.POST:
        data = refresh_content(website.url,website)
    else:
        delta = timezone.now() - website.last_visit
        delta = delta.total_seconds()/(3600*24)
        if(delta>1):
            # refresh cache
            data = refresh_content(website.url,website)
        else:
            if website.web_cache == 'length exceeded':
                data = refresh_content(website.url,website)
            elif website.web_cache == '':
                data = refresh_content(website.url,website)
            else:
                print("used cache")
                data = getInfo(website.web_cache)
    website.save()
    context = {
        'website' : website,
        'info_scrapped': data,
        'info_len': len(data),
    }
    return render(request,'contactkeep/website_view.html',context)

def getInfo(content):
    data = []
    import re
    from .classes import Info
    email_regex = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""",re.MULTILINE)
    emails = email_regex.findall(str(content))
    for email in emails:
        data.append(Info(email))
    phone_num_regex1 = re.compile(r"""\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$""")
    phone_nos = phone_num_regex1.findall(str(content))
    for phone_num in phone_nos:
        data.append(Info(phone_num))
    phone_num_regex2 = re.compile(r"""/(\+?( |-|\.)?\d{1,2}( |-|\.)?)?(\(?\d{3}\)?|\d{3})( |-|\.)?(\d{3}( |-|\.)?\d{4})/g""")
    phone_nos = phone_num_regex2.findall(str(content))
    for phone_num in phone_nos:
        data.append(Info(phone_num))
    phone_num_regex3 = re.compile(r"\+\d\d-\d\d\d-\d\d\d\d\d\d\d")
    phone_nos = phone_num_regex3.findall(str(content))
    for phone_num in phone_nos:
        data.append(Info(phone_num))
    phone_num_regex4 = re.compile(r"\+\d\d\s\d\d\d-\d\d\d\d\d\d\d")
    phone_nos = phone_num_regex4.findall(str(content))
    for phone_num in phone_nos:
        data.append(Info(phone_num))
    return data

def refresh_content(url,website):
    from .classes import Info
    data = []
    website_request=req.get(url=url)
    if (len(website_request.content)>99999):
        website.web_cache='length exceeded' 
    else:
        website.web_cache = website_request.content
    website.save()
    print("refreshing cache")
    data = getInfo(website_request.content)
    return data

def edit_website(request,website_id):
    website = get_object_or_404(Website,id=website_id)
    if 'edit-website' in request.POST:
        website.name = request.POST.get('name')
        website.url = request.POST.get('url')
        website.created_on = timezone.now()
        website.save()
        return HttpResponseRedirect('/websites/'+str(website_id)+'/')
    context = {
        'website' : website,
    }
    return render(request,'contactkeep/edit_website.html',context)