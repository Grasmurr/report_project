from django.urls import path
from . import views

urlpatterns = [
    path('api/promouter/<int:user_id>/', views.PromouterView.as_view(), name='get_promouter'),
    path('api/promouter/', views.PromouterView.as_view(), name='insert_promouter'),
    path('api/event/<str:name>/', views.EventView.as_view(), name='get_event'),
    path('api/event/', views.EventView.as_view(), name='insert_event'),
    path('api/ticket/<int:ticket_number>/', views.TicketView.as_view(), name='get_ticket'),
    path('api/ticket/', views.TicketView.as_view(), name='insert_ticket'),
]
