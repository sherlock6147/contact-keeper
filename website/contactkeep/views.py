from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Event

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
    all_events = Event.objects.all
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