from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

import json
from .models import Promouter, Event, Ticket
from .serializers import EventSerializer


import csv
from openpyxl import Workbook
from django.http import HttpResponse
from django.shortcuts import render


@method_decorator(csrf_exempt, name='dispatch')
class PromouterView(View):
    def post(self, request):
        data = json.loads(request.body)
        Promouter.objects.create(**data)
        return JsonResponse({'status': 'ok'}, status=201)

    def get(self, request, user_id=None):
        if user_id:
            promouter = Promouter.objects.filter(user_id=user_id).values()
            return JsonResponse({'data': list(promouter)}, safe=False)
        else:
            promouters = Promouter.objects.all().values()
            return JsonResponse({'data': list(promouters)}, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class PromouterUpdateView(View):
    def post(self, request, user_id):
        data = json.loads(request.body)
        promouter, created = Promouter.objects.update_or_create(
            user_id=user_id,
            defaults=data
        )
        status_code = 201 if created else 200  # 201 Created если объект был создан, иначе 200 OK
        return JsonResponse({'status': 'ok'}, status=status_code)

    def delete(self, request, user_id):
        try:
            promouter = Promouter.objects.get(user_id=user_id)
        except Promouter.DoesNotExist:
            return JsonResponse({'error': 'Promouter not found'}, status=404)

        promouter.delete()
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class EventView(View):
    def post(self, request):
        data = json.loads(request.body)
        Event.objects.create(**data)
        return JsonResponse({'status': 'ok'}, status=201)

    def get(self, request, name=None):
        if name:
            event = Event.objects.filter(name=name).values()
            return JsonResponse({'data': list(event)}, safe=False)
        else:
            events = Event.objects.all().values()
            return JsonResponse({'data': list(events)}, safe=False)


class EventAPIView(APIView):

    def get(self, request, name=None):
        if name:
            event = get_object_or_404(Event, name=name)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        return Response({'error': 'Name parameter is required'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class TicketView(View):
    def post(self, request):
        data = json.loads(request.body)
        Ticket.objects.create(**data)
        return JsonResponse({'status': 'ok'}, status=201)

    def get(self, request, ticket_number=None, ticket_type=None):
        if ticket_number:
            ticket = Ticket.objects.filter(ticket_number=ticket_number).values()
            return JsonResponse({'data': list(ticket)}, safe=False)
        elif ticket_type:
            tickets = Ticket.objects.filter(type=ticket_type).values()
            return JsonResponse({'data': list(tickets)}, safe=False)
        else:
            tickets = Ticket.objects.all().values()
            return JsonResponse({'data': list(tickets)}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TicketDeleteView(APIView):
    def delete(self, request, ticket_number=None):
        try:
            ticket = Ticket.objects.get(ticket_number=ticket_number)
        except Ticket.DoesNotExist:
            return JsonResponse({'error': 'Ticket not found'}, status=404)

        ticket.delete()
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class TicketExportCsv(View):
    def get(self, request, event_name):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tickets.csv"'

        writer = csv.writer(response)
        writer.writerow(['Ticket Number', 'Ticket Holder Name', 'Ticket Holder Surname', 'Ticket Type', 'Date of Birth', 'Price', 'Educational Program'])

        tickets = Ticket.objects.filter(event_name=event_name)
        for ticket in tickets:
            writer.writerow([ticket.ticket_number, ticket.ticket_holder_name, ticket.ticket_holder_surname, ticket.ticket_type, ticket.date_of_birth, ticket.price, ticket.educational_program])

        return response