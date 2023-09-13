import collections, os
from service.presentation import PresentationBuilder
from lxml import etree

def main():
    builder = PresentationBuilder()

    for i in range(1):
        slide = builder.create_slide()
        builder.grey_light_background(slide)
        builder.title_of_shmuts(slide)

    photos_info = collections.defaultdict(lambda: {'За работой': [], 'На площадке': []})

    for q, w, e in os.walk('downloaded_folders'):
        path_parts = str(q).split('/')
        if len(path_parts) == 3:
            name, place = path_parts[1], path_parts[2]
            for photo in e:
                if photo.endswith(('.jpg', '.png')):  # Проверяем, что это изображение
                    photos_info[name][place].append(os.path.join(q, photo))

    for name, places in photos_info.items():
        for place, photos in places.items():
            for i in range(0, len(photos), 2):  # Добавляем по два изображения на слайд
                left_photo = photos[i]
                right_photo = photos[i + 1] if i + 1 < len(photos) else None

                # TODO: Получить даты для изображений
                date_left = builder.date_for_photo_left
                date_right = builder.date_for_photo_right

                builder.create_photoslide(left_photo, date_left, place.lower(), right_photo, date_right)

    builder.prs.save('CC__title_sample.pptx')
    print("I am happy")


# cdef main():
# pass


if __name__ == '__main__':
    main()
