from django.urls import path

from . import views

app_name = 'contactkeep'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/',views.events,name='events'),
    path('event_edit/<int:event_id>/',views.event_edit,name="event_edit"),
]