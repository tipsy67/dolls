from dolls.models import Image, Product
from config.settings import IMG_HEIGHT, IMG_WIDTH
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image as PILImage
import os

def resize_and_crop_product_images(
        image,
        target_width: int = None,
        target_height: int = None,
        quality: int = 100,
        crop_if_needed: bool = True,
) -> None:
    print(image)
    print(image.image)
    with PILImage.open(image.image) as img:
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        original_width, original_height = img.size

        if target_width == original_width and target_height == original_height:
            return

        if not target_width and not target_height:
            return

        ratio_width = target_width / original_width
        ratio_height = target_height / original_height

        if ratio_width > ratio_height:
            new_width = target_width
            new_height = int(original_height * ratio_width)
        else:
            new_width = int(original_width * ratio_height)
            new_height = target_height

        img = img.resize((new_width, new_height), PILImage.Resampling.LANCZOS)

        if crop_if_needed and (
                new_width != target_width or new_height != target_height
        ):
            left = (new_width - target_width) / 2
            top = (new_height - target_height) / 2
            right = (new_width + target_width) / 2
            bottom = (new_height + target_height) / 2
            img = img.crop((left, top, right, bottom))

        # Сохраняем в WebP
        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=quality)

        # Обновляем файл
        original_name = f"{os.path.splitext(os.path.basename(image.image.name))[0]}.webp"
        image.image.save(
            original_name, ContentFile(buffer.getvalue()), save=False
        )
        image.name = original_name
        image.save()


def resize_product_image(image_id):
    image = Image.objects.filter(pk=image_id).first()
    if image:
        resize_and_crop_product_images(
        image, target_width=IMG_WIDTH, target_height=IMG_HEIGHT)


def resize_product_images(product_id: int) -> None:
    product = Product.objects.prefetch_related('images').get(pk=product_id)
    images = product.images.all()
    for image in images:
        try:
            resize_and_crop_product_images(
                image, target_width=IMG_WIDTH, target_height=IMG_HEIGHT
            )
        except Exception as e:
            print(f"Ошибка обработки изображения {image.id}: {str(e)}")
            continue
