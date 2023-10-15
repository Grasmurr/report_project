from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Promouter, Event, Ticket


@method_decorator(csrf_exempt, name='dispatch')
class PromouterView(View):
    def post(self, request):
        data = json.loads(request.body)
        Promouter.objects.create(**data)
        return JsonResponse({'status': 'ok'}, status=201)

    def get(self, request, user_id):
        promouter = Promouter.objects.filter(user_id=user_id).values()
        return JsonResponse({'data': list(promouter)}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class EventView(View):
    def post(self, request):
        data = json.loads(request.body)
        Event.objects.create(**data)
        return JsonResponse({'status': 'ok'}, status=201)

    def get(self, request, name):
        event = Event.objects.filter(name=name).values()
        return JsonResponse({'data': list(event)}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TicketView(View):
    def post(self, request):
        data = json.loads(request.body)
        Ticket.objects.create(**data)
        return JsonResponse({'status': 'ok'}, status=201)

    def get(self, request, ticket_number):
        ticket = Ticket.objects.filter(ticket_number=ticket_number).values()
        return JsonResponse({'data': list(ticket)}, safe=False)
