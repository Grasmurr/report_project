import collections, os, datetime, random
from service.presentation import PresentationBuilder
from service.telegram_bot.main import start_bot
import asyncio
import logging
import sys


def generate_random_time(date_str):
    try:
        if '.' in date_str:
            date_obj = datetime.datetime.strptime(date_str, "%d.%m.%Y")
        elif '_' in date_str:
            date_obj = datetime.datetime.strptime(date_str, "%d_%m_%Y")
        elif '-' in date_str:
            date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")

    except:
        return False

    random_hour = random.randint(11, 19)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    datetime_obj = date_obj + datetime.timedelta(hours=random_hour, minutes=random_minute, seconds=random_second)

    return '.'.join(str(str(date_obj).split()[0]).split('-')[::-1]) + '\n' + str(datetime_obj.strftime("%H:%M:%S")) + '\nМосква'

def main():
    builder = PresentationBuilder()

    for i in range(1):
        slide = builder.create_slide()
        builder.grey_light_background(slide)
        builder.title_of_shmuts(slide)

    photos_info = {}

    for q, w, e in os.walk('downloaded_folders'):
        path_parts = str(q).split('/')
        if len(path_parts) == 3:
            name, place = path_parts[1], path_parts[2]
            name = name.lower()
            place = place.lower()

            if name not in photos_info:
                photos_info[name] = {'за работой': [], 'на площадке': []}

            for photo in e:
                if 'за' in place:
                    photos_info[name]['за работой'].append(os.path.join(q, photo))
                else:
                    photos_info[name]['на площадке'].append(os.path.join(q, photo))

    for name, places in photos_info.items():
        for place, photos in places.items():
            for i in range(0, len(photos), 2):  # Добавляем по два изображения на слайд
                left_photo = photos[i]
                right_photo = photos[i + 1] if i + 1 < len(photos) else None

                # TODO: Получить даты для изображений
                date_left = generate_random_time('.'.join(left_photo.split('/')[-1].split('.')[:-1])[-10:])
                # print(left_photo, '.'.join(left_photo.split('/')[-1].split('.')[:-1])[-10:])
                if not date_left:
                    print(f'Для {left_photo} дата не добавилась')
                if right_photo:
                    date_right = generate_random_time('.'.join(right_photo.split('/')[-1].split('.')[:-1])[-10:])
                builder.create_photoslide(left_photo, date_left, place.lower(), right_photo, date_right)

    builder.prs.save('CC__title_sample.pptx')
    print("I am happy")


# cdef main():
# pass
def func():
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())
    main()
