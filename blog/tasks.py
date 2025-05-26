from celery import shared_task

from blog.src.requests_to_ai import generate_content
from blog.src.images import resize_article_image

@shared_task
def remake_article(product_id: int):
    generate_content(product_id)


@shared_task
def resize_image(article_id:int) -> None:
    resize_article_image(article_id)