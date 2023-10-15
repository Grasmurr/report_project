from django.urls import path
from . import views

urlpatterns = [
    path('promouter/<int:user_id>/', views.PromouterView.as_view(), name='get_promouter'),
    path('promouter/', views.PromouterView.as_view(), name='insert_promouter'),
    path('event/<str:name>/', views.EventView.as_view(), name='get_event'),
    path('event/', views.EventView.as_view(), name='insert_event'),
    path('ticket/<int:ticket_number>/', views.TicketView.as_view(), name='get_ticket'),
    path('ticket/', views.TicketView.as_view(), name='insert_ticket'),
]
