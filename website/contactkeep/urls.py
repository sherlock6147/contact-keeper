from django.urls import path

from . import views

app_name = 'contactkeep'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/',views.events,name='events'),
    path('events/<int:event_id>/edit',views.event_edit,name="event_edit"),
    path('events/<int:event_id>/',views.event_details,name="event_details"),
    path('websites/',views.websites,name="websites"),
    path('websites/<int:website_id>/',views.website_view,name="view_website"),
    path('websites/<int:website_id>/edit',views.edit_website,name="website_edit"),
]