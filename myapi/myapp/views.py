from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
from .models import Promouter, Event, Ticket
from .serializers import EventSerializer

import csv
from openpyxl import Workbook
from django.http import HttpResponse
from django.shortcuts import render
import openpyxl


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
class EventCreateOrUpdateView(View):
    def post(self, request, name):
        data = json.loads(request.body)

        event, created = Event.objects.get_or_create(name=name)

        fields_to_update = {}
        for key, value in data.items():
            if hasattr(event, key) and value is not None:
                fields_to_update[key] = value

        if fields_to_update:
            for key, value in fields_to_update.items():
                setattr(event, key, value)
            event.save(update_fields=fields_to_update.keys())

        status_code = 201 if created else 200
        return JsonResponse({'status': 'ok'}, status=status_code)



@method_decorator(csrf_exempt, name='dispatch')
class TicketView(View):
    def post(self, request):
        data = json.loads(request.body)
        Ticket.objects.create(**data)
        return JsonResponse({'status': 'ok'}, status=201)

    def get(self, request, ticket_number=None, ticket_type=None):
        event = request.GET.get('event')
        if not event:
            return JsonResponse({'error': 'Event parameter is required'}, status=400)

        ticket_type = request.GET.get('ticket_type')
        ticket_number = request.GET.get('ticket_number')

        filters = {'event': event}

        if ticket_type:
            filters['ticket_type'] = ticket_type
        if ticket_number:
            filters['ticket_number'] = ticket_number

        tickets = Ticket.objects.filter(**filters).values()
        return JsonResponse({'data': list(tickets)}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TicketUpdateView(APIView):
    def post(self, request, event, ticket_number, ticket_type):
        new_price = request.data.get('new_price')
        if new_price is None:
            return Response({'error': 'New price is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket = Ticket.objects.get(event=event, ticket_number=ticket_number, ticket_type=ticket_type)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        ticket.is_refunded = True
        ticket.price = new_price
        ticket.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class IncrementView(View):

    def post(self, request, name, field):
        event = get_object_or_404(Event, name=name)
        if field == 'nm_prime':
            event.nm_prime += 1
        elif field == 'nm_usual':
            event.nm_usual += 1
        elif field == 'nm_deposit':
            event.nm_deposit += 1
        else:
            return JsonResponse({'error': 'Invalid field'}, status=400)
        event.save()
        return JsonResponse({'success': True}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class DecrementView(View):

    def post(self, request, name, field):
        event = get_object_or_404(Event, name=name)
        if field == 'nm_prime':
            event.nm_prime -= 1
        elif field == 'nm_usual':
            event.nm_usual -= 1
        elif field == 'nm_deposit':
            event.nm_deposit -= 1
        else:
            return JsonResponse({'error': 'Invalid field'}, status=400)
        event.save()
        return JsonResponse({'success': True}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ToggleEventHiddenStatusView(View):
    def post(self, request, name):
        try:
            event = Event.objects.get(name=name)
            # Измените эту строку для работы с JSON
            data = json.loads(request.body)
            is_hidden = data.get('is_hidden')  # Теперь это должно работать с JSON

            if is_hidden is not None and is_hidden in ['true', 'false']:
                is_hidden = bool(is_hidden.capitalize())
                event.is_hidden = is_hidden
                event.save()
                return JsonResponse({'status': 'ok'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid is_hidden value'}, status=400)
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)



# class ExportTicketsView(APIView):
#     def get(self, request, format='.xlsx', event='SKYNET'):
#
#
#         tickets = Ticket.objects.filter(event=event)
#
#         if format == '.csv':
#             response = JsonResponse(content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="tickets.csv"'
#
#             writer = csv.writer(response)
#             writer.writerow(['Ticket Number', 'Ticket Holder Name', 'Ticket Holder Surname', 'Ticket Type', 'Date of Birth', 'Price', 'Educational Program', 'Educational Course'])
#
#             for ticket in tickets:
#                 writer.writerow([ticket.ticket_number, ticket.ticket_holder_name, ticket.ticket_holder_surname, ticket.ticket_type, ticket.date_of_birth, ticket.price, ticket.educational_program, ticket.educational_course])
#
#             return response
#
#         elif format == '.xlsx':
#             response = JsonResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             response['Content-Disposition'] = 'attachment; filename="tickets.xlsx"'
#
#             workbook = openpyxl.Workbook()
#             worksheet = workbook.active
#
#             worksheet.append(['Ticket Number', 'Ticket Holder Name', 'Ticket Holder Surname', 'Ticket Type', 'Date of Birth', 'Price', 'Educational Program', 'Educational Course'])
#
#             for ticket in tickets:
#                 worksheet.append([ticket.ticket_number, ticket.ticket_holder_name, ticket.ticket_holder_surname, ticket.ticket_type, ticket.date_of_birth, ticket.price, ticket.educational_program, ticket.educational_course])
#
#             workbook.save(response)
#
#             return response
