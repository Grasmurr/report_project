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


async def create_event(name, nm_prime, nm_usual):
    endpoint = 'event/'
    data = {
        'name': name,
        'nm_prime': nm_prime,
        'nm_usual': nm_usual
    }
    return await send_to_api(endpoint, data)


async def create_ticket(Event, ticket_number, name, surname, ticket_type, date_of_birth, price, educational_program, educational_course):
    endpoint = 'ticket/'

    data = {
        'event': Event,
        'ticket_number': ticket_number,
        'ticket_holder_name': name,
        'ticket_holder_surname': surname,
        'ticket_type': ticket_type,
        'date_of_birth': date_of_birth,
        'price': price,
        'educational_program': educational_program,
        'educational_course': educational_course
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


async def get_all_tickets():
    endpoint = 'tickets/'
    return await get_from_api(endpoint)


async def get_tickets_by_type(ticket_type):
    endpoint = f'tickets/{ticket_type}/'
    return await get_from_api(endpoint)


async def get_event_by_name(name):
    endpoint = f'get_event/{name}/'
    return await get_from_api(endpoint)


async def get_ticket_by_number(ticket_number):
    endpoint = f'get_ticket/{ticket_number}/'
    return await get_from_api(endpoint)

async def delete_ticket(ticket_number):
    endpoint = f'tickets/{ticket_number}/'
    return await send_to_api(endpoint, None)




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
    # Удалите None значения из данных
    data = {k: v for k, v in data.items() if v is not None}
    return await send_to_api(endpoint, data)


async def delete_promouter(user_id):
    endpoint = f'promouter/{user_id}/'
    return await send_to_api(endpoint, method='DELETE')
