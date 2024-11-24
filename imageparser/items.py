# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose, Join


def process_images(value):
    images = []

    # Если в строке несколько URL-ов (например, srcset)
    if ',' in value:
        urls = [url.strip() for url in value.split(',')]
        for url in urls:
            image_url = url.split(' ')[0]  # Получаем URL до первого пробела
            image_url = add_extension_if_needed(image_url)  # Добавляем расширение, если нужно
            image_url = add_scheme_if_needed(image_url)  # Добавляем схему, если нужно
            images.append(image_url)
    else:
        # Если это одиночный URL
        value = add_extension_if_needed(value)  # Добавляем расширение, если нужно
        value = add_scheme_if_needed(value)  # Добавляем схему, если нужно
        images.append(value)

    # Выбор URL с максимальным разрешением
    if images:
        max_resolution_image = max(images, key=extract_width)
        return [max_resolution_image]  # Возвращаем список с одним элементом (URL с максимальным разрешением)
    return images

# Функция для извлечения параметра ширины из URL (если доступен)
def extract_width(url):
    match = re.search(r'w=(\d+)', url)
    if match:
        return int(match.group(1))
    return 0  # Возвращаем 0, если ширина не указана

# Функция для добавления расширения, если оно отсутствует
def add_extension_if_needed(url):
    if not re.search(r'\.\w{3,4}$', url):
        url += '.jpg'  # Добавляем .jpg по умолчанию
    return url

# Функция для добавления схемы (https://) в URL, если она отсутствует
def add_scheme_if_needed(url):
    if url.startswith('//'):
        url = 'https:' + url
    elif not re.match(r'^https?://', url):
        url = 'https://' + url
    return url



class ImageparserItem(scrapy.Item):
    print()
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_name = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(process_images),output_processor=TakeFirst())
    image_paths = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
