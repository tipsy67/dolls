import os

from openai import OpenAI

from blog.models import BlogArticle
from config.settings import BASE_DIR
from dolls.models import Product


def generate_content(product_id: int) -> None:
    DEEPSEEK_API_URL = "https://api.deepseek.com/"
    API_KEY = os.environ.get("DEEPSEEK_API_KEY")
    TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "article-for-ai.html")

    article = BlogArticle.objects.filter(id=product_id).first()

    if not article:
        return

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as file:
        html_template = file.read()

    prompt = f"""
    Ты профессиональный верстальщик HTML. Преобразуй текст статьи блога в HTML-блоки, 
    которые будут соответствовать стилям и структуре указанного шаблона. 
    Стиль изложения и содержимое оставь без изменений.

    === ШАБЛОН ===
    {html_template}
    === КОНЕЦ ШАБЛОНА ===

    === ОПИСАНИЕ ТОВАРА ===
    {article.content}
    === КОНЕЦ ОПИСАНИЯ ===

    Верни в ответе чистый HTML без всяких примечаний.
    """

    client = OpenAI(api_key=API_KEY, base_url=DEEPSEEK_API_URL)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Ты профессиональный верстальщик HTML."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )

    new_article = response.choices[0].message.content

    article.content = new_article
    article.save()
