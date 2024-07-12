# tasks.py

from celery import shared_task
from .models import Product

@shared_task
def bulk_upload_task(product_ids):
    products = Product.objects.filter(id__in=product_ids)
    for product in products:
        Product.objects.create(**product)

