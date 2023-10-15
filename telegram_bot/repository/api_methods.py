import aiohttp
import json

############################################################################################################
##                                                                                                        ##
##                                          POST METHODS                                                  ##
##                                                                                                        ##
############################################################################################################


async def send_to_api(endpoint, data):
    url = f'http://django_app:8000/api/{endpoint}'
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data), headers=headers) as response:
            if response.status != 200:
                # Handle error
                response_data = await response.text()
                print(f"Error: {response.status}. {response_data}")
            else:
                return await response.json()


async def create_promouter(user_id, username, full_name):
    endpoint = 'promouter/'
    data = {
        'user_id': user_id,
        'username': username,
        'full_name': full_name
    }
    return await send_to_api(endpoint, data)


async def create_event(name, nm_prime, nm_usual):
    endpoint = 'event/'
    data = {
        'name': name,
        'nm_prime': nm_prime,
        'nm_usual': nm_usual
    }
    return await send_to_api(endpoint, data)


async def create_ticket(event_name, ticket_number, name, surname, ticket_type):
    endpoint = 'ticket/'
    data = {
        'event_name': event_name,
        'ticket_number': ticket_number,
        'name': name,
        'surname': surname,
        'ticket_type': ticket_type
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
    url = f'http://django_app:8000/api/{endpoint}'

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
    endpoint = f'promouter/{user_id}/'
    return await get_from_api(endpoint)


async def get_all_events():
    endpoint = 'events/'
    return await get_from_api(endpoint)


async def get_all_tickets():
    endpoint = 'tickets/'
    return await get_from_api(endpoint)


async def get_tickets_by_type(ticket_type):
    endpoint = f'tickets/{ticket_type}/'
    return await get_from_api(endpoint)


async def get_event_by_name(name):
    endpoint = f'event/{name}/'
    return await get_from_api(endpoint)


async def get_ticket_by_number(ticket_number):
    endpoint = f'ticket/{ticket_number}/'
    return await get_from_api(endpoint)


'''
Пример использования:
ticket_number = '123'
ticket_data = await get_ticket_by_number(ticket_number)
'''