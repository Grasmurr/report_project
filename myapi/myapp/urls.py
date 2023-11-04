from django.urls import path
from . import views
from .views import EventAPIView#, ExportTicketsView

urlpatterns = [
    path('get_promouter/<int:user_id>/', views.PromouterView.as_view(), name='get_promouter'),
    path('promouter/', views.PromouterView.as_view(), name='insert_promouter'),
    path('promouters/', views.PromouterView.as_view(), name='get_all_promouters'),
    path('promouter/<int:user_id>/', views.PromouterUpdateView.as_view(), name='promouter_update_delete'),

    path('get_event/<str:name>/', views.EventView.as_view(), name='get_event'),
    path('event/', views.EventView.as_view(), name='insert_event'),
    path('events/', views.EventView.as_view(), name='get_all_events'),
    path('event/<str:name>/', EventAPIView.as_view(), name='api_event_detail'),
    path('event/<str:name>/increment/<str:field>/', views.IncrementView.as_view(), name='increment'),
    path('event/<str:name>/decrement/<str:field>/', views.DecrementView.as_view(), name='decrement'),
    path('event_prices/<str:name>/', views.EventCreateOrUpdateView.as_view(), name='event-create-or-update'),
    path('events/<str:name>/toggle_hidden/', views.ToggleEventHiddenStatusView.as_view(), name='toggle_event_hidden'),

    path('get_ticket/<int:ticket_number>/', views.TicketView.as_view(), name='get_ticket'),
    path('ticket/', views.TicketView.as_view(), name='insert_ticket'),
    path('tickets/', views.TicketView.as_view(), name='get_all_tickets'),
    path('ticket_delete/<str:event>/<int:ticket_number>/<str:ticket_type>/', views.TicketDeleteView.as_view(),
         name='delete_ticket'),


    # path('export-tickets/', views.ExportTicketsView.as_view(), name ='export_tickets_csv')

]
