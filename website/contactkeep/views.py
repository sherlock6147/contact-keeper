from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Event

# Create your views here.

def home(request):
    current_event = Event.objects.filter(current=True)
    current_event = current_event[0]
    context = {
        'event' : current_event,
    }
    return render(request,'contactkeep/home.html',context)

def events(request):
    all_events = Event.objects.all
    context = {
        'list_of_events' : all_events,
    }
    return render(request,'contactkeep/events.html',context)

def event_edit(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    context = {
        'event' : event,
    }
    return render(request,'contactkeep/edit.html',context)