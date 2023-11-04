import aiohttp
import json
import csv


############################################################################################################
##                                                                                                        ##
##                                          POST METHODS                                                  ##
##                                                                                                        ##
############################################################################################################


async def send_to_api(endpoint, data=None, method='POST'):
    url = f'http://djangoapp:8000/api/{endpoint}'
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        if method == 'POST':
            async with session.post(url=url, data=json.dumps(data), headers=headers) as response:
                if response.status != 200:
                    # Handle error
                    response_data = await response.text()
                    print(f"Error: {response.status}. {response_data}")
                else:
                    return await response.json()
        elif method == 'DELETE':
            async with session.delete(url=url, headers=headers) as response:
                if response.status != 200:
                    # Handle error
                    response_data = await response.text()
                    print(f"Error: {response.status}. {response_data}")
                else:
                    return await response.json()


async def create_promouter(user_id, username, full_name, phone_number):
    endpoint = 'promouter/'
    data = {
        'user_id': user_id,
        'username': username,
        'full_name': full_name,
        'phone_number': phone_number
    }
    return await send_to_api(endpoint, data)


async def create_event(name, nm_prime, nm_usual, event_date, prices):
    endpoint = 'event/'
    data = {
        'name': name,
        'nm_prime': nm_prime,
        'nm_usual': nm_usual,
        'date_of_event': event_date,
        'prices': prices
    }
    return await send_to_api(endpoint, data)


async def create_ticket(event, ticket_number, name, surname, ticket_type, date_of_birth, price, educational_program,
                        educational_course, phone_number):
    endpoint = 'ticket/'

    data = {
        'event': event,
        'ticket_number': ticket_number,
        'ticket_holder_name': name,
        'ticket_holder_surname': surname,
        'ticket_type': ticket_type,
        'date_of_birth': date_of_birth,
        'price': price,
        'educational_program': educational_program,
        'educational_course': educational_course,
        'phone_number': phone_number
    }
    return await send_to_api(endpoint, data)

'''
Пример использования:
user_id = 12345
username = 'example_user'
full_name = 'Example User'
await create_promouter(user_id, username, full_name)
'''
############################################################################################################
##                                                                                                        ##
##                                          GET METHODS                                                   ##
##                                                                                                        ##
############################################################################################################


async def get_from_api(endpoint, params=None):
    url = f'http://djangoapp:8000/api/{endpoint}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch data from API. Status: {response.status}")
                return None


async def get_all_promouters():
    endpoint = 'promouters/'
    return await get_from_api(endpoint)


async def get_promouter(user_id):
    endpoint = f'get_promouter/{user_id}/'
    return await get_from_api(endpoint)


async def get_all_events():
    endpoint = 'events/'
    return await get_from_api(endpoint)


# async def get_all_tickets(event=None):
#     endpoint = 'tickets/'
#     return await get_from_api(endpoint)


async def get_ticket_by_number_or_type(event, ticket_number=None, ticket_type=None):
    endpoint = 'tickets/'
    params = {'event': event}
    if ticket_number:
        params['ticket_number'] = ticket_number
    if ticket_type:
        params['ticket_type'] = ticket_type
    return await get_from_api(endpoint, params=params)


async def get_event_by_name(name):
    endpoint = f'get_event/{name}/'
    return await get_from_api(endpoint)


async def get_event(name):
    endpoint = f'event/{name}/'
    return await get_from_api(endpoint)


# async def get_tickets_by_event(event_name):
#     all_tickets = await get_all_tickets()
#     return [ticket for ticket in all_tickets['data'] if ticket['event'] == event_name]



'''
Пример использования:
ticket_number = '123'
ticket_data = await get_ticket_by_number(ticket_number)
'''

############################################################################################################
##                                                                                                        ##
##                                          PUT METHODS                                                   ##
##                                                                                                        ##
############################################################################################################


async def update_promouter(user_id, username=None, full_name=None, phone_number=None):
    endpoint = f'promouter/{user_id}/'
    data = {
        'user_id': user_id,
        'username': username,
        'full_name': full_name,
        'phone_number': phone_number
    }
    data = {k: v for k, v in data.items() if v is not None}
    return await send_to_api(endpoint, data)


async def update_ticket_number(event_name, field, action):
    endpoint = f'event/{event_name}/{action}/{field}/'
    await send_to_api(endpoint, method='POST')


async def update_event_data(name, nm_prime=None, nm_usual=None, event_date=None, prices=None):
    endpoint = f'event_prices/{name}/'
    data = {
        'name': name,
        'nm_prime': nm_prime,
        'nm_usual': nm_usual,
        'date_of_event': event_date,
        'prices': prices
    }
    clean_data = {k: v for k, v in data.items() if v is not None}
    return await send_to_api(endpoint, clean_data, method='POST')


async def update_event_visibility(event_name, is_hidden):
    url = f'events/{event_name}/toggle_hidden/'
    data = {'is_hidden': str(is_hidden)}
    response = await send_to_api(url, data)
    return response


############################################################################################################
##                                                                                                        ##
##                                          DELETE METHODS                                                ##
##                                                                                                        ##
############################################################################################################


async def delete_promouter(user_id):
    endpoint = f'promouter/{user_id}/'
    return await send_to_api(endpoint, method='DELETE')


async def delete_ticket(event, ticket_number, ticket_type):
    endpoint = f'ticket_delete/{event}/{ticket_number}/{ticket_type}/'
    return await send_to_api(endpoint, method='DELETE')


