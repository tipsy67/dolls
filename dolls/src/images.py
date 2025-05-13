from config.settings import IMG_HEIGHT, IMG_WIDTH
from dolls.models import Product, Image
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image as PILImage
import os


def resize_and_crop_product_images(
    image: Image,
    target_width: int = None,
    target_height: int = None,
    quality: int = 100,
    crop_if_needed: bool = True,
) -> None:
    with PILImage.open(image.image) as img:
        # Конвертируем в RGB при необходимости
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        original_width, original_height = img.size

        # Если не указаны размеры - пропускаем
        if not target_width and not target_height:
            return

        # Пропорциональное изменение размера
        if target_width and target_height:
            # Рассчитываем соотношения сторон
            target_ratio = target_width / target_height
            original_ratio = original_width / original_height

            # Определяем, по какой стороне ресайзить
            if original_ratio > target_ratio:
                # Шире целевого - ресайзим по ширине
                new_width = target_width
                new_height = int(target_width / original_ratio)
            else:
                # Выше целевого - ресайзим по высоте
                new_height = target_height
                new_width = int(target_height * original_ratio)

            img = img.resize((new_width, new_height), PILImage.Resampling.LANCZOS)

            # Обрезка до точных размеров, если требуется
            if crop_if_needed and (
                new_width != target_width or new_height != target_height
            ):
                left = (new_width - target_width) / 2
                top = (new_height - target_height) / 2
                right = (new_width + target_width) / 2
                bottom = (new_height + target_height) / 2
                img = img.crop((left, top, right, bottom))

        elif target_width:
            # Только ширина - меняем пропорционально
            ratio = target_width / original_width
            new_height = int(original_height * ratio)
            img = img.resize((target_width, new_height), PILImage.Resampling.LANCZOS)

        elif target_height:
            # Только высота - меняем пропорционально
            ratio = target_height / original_height
            new_width = int(original_width * ratio)
            img = img.resize((new_width, target_height), Image.LANCZOS)

        # Сохраняем в WebP
        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=quality)

        # Обновляем файл
        original_name = os.path.splitext(image.image.name)[0]
        image.image.save(
            f"{original_name}.webp", ContentFile(buffer.getvalue()), save=False
        )
        image.save()


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
