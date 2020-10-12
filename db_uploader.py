import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kneetag.settings")
django.setup()

from product.models import Product, Category, Series, Size, SubImage, Type, Detail

CSV_PATH_PRODUCTS = './kneetag_final_3.csv'

category = Category.objects.create(name='shirt')
category_id = category.id
type_detail = Type.objects.create(name='detail')
style_detail = Type.objects.create(name='style')

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        series_name = row[0]
        name = row[1]
        image_url=row[2]
        price = row[3]
        sizes=row[4].strip('[]').split(',')
        new_sizes = [
                size.strip("'’‘").strip(" ‘’").strip("'") for size in sizes 
                if "'" in size or "‘" in size or "’" in size
            ]
        sub_detail = row[5]
        detail_title=row[6].strip('[]').split(',')
        new_detail_title = [
                title.strip("'’‘").strip(" ‘’").strip("'") for title in detail_title 
                if "'" in title or "‘" in title or "’" in title
        ]
        detail_content=row[7].strip('[]').split(',')
        new_detail_content = [
                content.strip("'’‘").strip(" ‘’").strip("'") for content in detail_content 
                if "'" in content or "‘" in content or "’" in content
        ]
        sub_image_detail=row[8]
        sub_image_style=row[9]

        if Series.objects.filter(name=series_name).exists():
            series = Series.objects.get(name=series_name)
            product = Product.objects.create(name=name, image_url=image_url, series_id=series.id)
            for i in range(len(new_detail_title)):
                title = f"{i} {new_detail_title[i]}"
                content = f"{i} {new_detail_content[i]}"
                Detail.objects.create(title=title, content=content, series_id=series.id)
            SubImage.objects.create(image_url=sub_image_detail, product_id=product.id, type_id=type_detail.id)
            SubImage.objects.create(image_url=sub_image_style, product_id=product.id, type_id=style_detail.id)
            for size in new_sizes:
                Size.objects.create(name=size, series_id=series.id)
        else:
            series = Series.objects.create(name=series_name, category_id=category_id, price=price, sub_detail=sub_detail)
            product = Product.objects.create(name=name, image_url=image_url, series_id=series.id)
            for i in range(len(new_detail_title)):
                title = f"{i} {new_detail_title[i]}"
                content = f"{i} {new_detail_content[i]}"
                Detail.objects.create(title=title, content=content, series_id=series.id)
            SubImage.objects.create(image_url=sub_image_detail, product_id=product.id, type_id=type_detail.id)
            SubImage.objects.create(image_url=sub_image_style, product_id=product.id, type_id=style_detail.id)
            for size in new_sizes:
                Size.objects.create(name=size, series_id=series.id)
