from django.urls import path
from . import views

urlpatterns = [
    path('get_promouter/<int:user_id>/', views.PromouterView.as_view(), name='get_promouter'),
    path('promouter/', views.PromouterView.as_view(), name='insert_promouter'),
    path('promouters/', views.PromouterView.as_view(), name='get_all_promouters'),

    path('get_event/<str:name>/', views.EventView.as_view(), name='get_event'),
    path('event/', views.EventView.as_view(), name='insert_event'),
    path('events/', views.EventView.as_view(), name='get_all_events'),

    path('get_ticket/<int:ticket_number>/', views.TicketView.as_view(), name='get_ticket'),
    path('ticket/', views.TicketView.as_view(), name='insert_ticket'),
    path('tickets/', views.TicketView.as_view(), name='get_all_tickets'),
    path('tickets/<str:ticket_type>/', views.TicketView.as_view(), name='get_tickets_by_type'),
    path('tickets/<int:ticket_number>/', views.TicketView.as_view(), name='delete_ticket')
]
