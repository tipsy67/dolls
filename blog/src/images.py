from blog.models import BlogArticle
from dolls.src.images import resize_and_crop_product_images


def resize_article_image(article_id):
    image = BlogArticle.objects.filter(pk=article_id).first()
    if image:
        resize_and_crop_product_images(
        image, target_width=1024, target_height=1024)