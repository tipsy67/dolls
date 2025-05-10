from celery import shared_task

from blog.src.requests_to_ai import generate_content


@shared_task
def remake_article(product_id: int):
    generate_content(product_id)
