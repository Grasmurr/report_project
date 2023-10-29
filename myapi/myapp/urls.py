from django.urls import path
from . import views
from .views import EventAPIView, ExportTicketsView

urlpatterns = [
    path('get_promouter/<int:user_id>/', views.PromouterView.as_view(), name='get_promouter'),
    path('promouter/', views.PromouterView.as_view(), name='insert_promouter'),
    path('promouters/', views.PromouterView.as_view(), name='get_all_promouters'),
    path('promouter/<int:user_id>/', views.PromouterUpdateView.as_view(), name='promouter_update_delete'),

    path('get_event/<str:name>/', views.EventView.as_view(), name='get_event'),
    path('event/', views.EventView.as_view(), name='insert_event'),
    path('events/', views.EventView.as_view(), name='get_all_events'),
    path('event/<str:name>/', EventAPIView.as_view(), name='api_event_detail'),

    path('get_ticket/<int:ticket_number>/', views.TicketView.as_view(), name='get_ticket'),
    path('ticket/', views.TicketView.as_view(), name='insert_ticket'),
    path('tickets/', views.TicketView.as_view(), name='get_all_tickets'),
    path('tickets/<int:ticket_type>/', views.TicketView.as_view(), name='get_tickets_by_type'),
    path('ticket_delete/<int:ticket_number>/', views.TicketDeleteView.as_view(), name='delete_ticket'),

    path('export_tickets/', views.ExportTicketsView.as_view(), name='export_tickets_csv')

]
