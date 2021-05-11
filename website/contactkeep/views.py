from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, request
from .models import *
from django.utils import timezone
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
    website.save()
    context = {
        'website' : website,
    }
    return render(request,'contactkeep/website_view.html',context)

def edit_website(request,website_id):
    website = get_object_or_404(Website,id=website_id)
    if 'edit-website' in request.POST:
        website.name = request.POST.get('name')
        website.url = request.POST.get('url')
        website.created_on = timezone.now()
        website.save()
    context = {
        'website' : website,
    }
    return render(request,'contactkeep/edit_website.html',context)