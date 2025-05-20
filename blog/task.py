from celery import shared_task

from blog.src.images import resize_article_image


@shared_task
def resize_image(article_id:int) -> None:
    resize_article_image(article_id)