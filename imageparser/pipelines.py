# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os
from typing import Any
from itemadapter import ItemAdapter
import scrapy
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse




class ImageparserPipeline:
    def process_item(self, item, spider):
        print()
        return item
    
class ImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # Проверяем, что поле 'images' присутствует и это список
        if item.get('images') and isinstance(item['images'], list):
            for img_url in item['images']:
                if self.is_valid_url(img_url):
                    try:
                        yield scrapy.Request(img_url)
                    except Exception as e:
                        print(f'Error getting image: {e}')
                else:
                    print(f'Invalid URL: {img_url}')
        # Если 'images' не является списком, проверяем, есть ли строковый URL
        elif isinstance(item.get('images'), str) and self.is_valid_url(item['images']):
            try:
                yield scrapy.Request(item['images'])
            except Exception as e:
                print(f'Error getting image: {e}')
        else:
            print('No valid image URLs found in item.')

    def is_valid_url(self, url):
        """Функция для проверки корректности URL-адреса."""
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])

    def item_completed(self, results, item, info):
        if results:
            image_paths = [itm[1]['path'] for itm in results if itm[0]]
            if image_paths:
                item['image_paths'] = image_paths
        return item
    
class CsvPipeline:

    def open_spider(self, spider):
        # Проверяем, существует ли файл перед его открытием
        file_exists = os.path.isfile('images_data.csv')
        # Открываем файл в режиме добавления (append)
        self.file = open('images_data.csv', 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        
        # Записываем заголовки, только если файл новый
        if not file_exists:
            self.writer.writerow(['Category', 'Image Name', 'Local Path', 'Image URL'])

    def process_item(self, item, spider):
        # Получаем данные об изображении для записи
        category = item.get('category', 'N/A')
        image_name = item.get('image_name', 'N/A')
        image_paths = item.get('image_paths', ['N/A'])
        image_urls = item.get('images', 'N/A')

        # Записываем в CSV-файл построчно
        for path in image_paths:
            self.writer.writerow([category, image_name, path, image_urls])
        
        return item

    def close_spider(self, spider):
        # Закрываем файл при завершении работы паука
        self.file.close()
