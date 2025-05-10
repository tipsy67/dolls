import os
import subprocess
import time
from datetime import datetime

import instaloader
import requests
from celery import shared_task

from config.settings import MEDIA_ROOT, STATIC_FILES
from dolls.src.mailers import sendmail_cmd
from dolls.src.requests_to_ai import generate_description


@shared_task
def sendmail(recipients_emails: list, title: str, content: str):
    sendmail_cmd(recipients_emails, title, content)


@shared_task
def remake_description(product_id: int):
    generate_description(product_id)


def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json()["ip"]
    except:
        return "Не удалось определить IP"


def download_and_rename_posts():
    target_username = 'ekaterinas_toyland'

    # Настройка Instaloader
    loader = instaloader.Instaloader(
        dirname_pattern=os.path.join(MEDIA_ROOT, 'insta', target_username),
        save_metadata=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        compress_json=False,
        filename_pattern="{shortcode}",
    )

    # Создаем папку для сохранения
    os.makedirs(target_username, exist_ok=True)

    # Получаем профиль
    try:
        profile = instaloader.Profile.from_username(loader.context, target_username)
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    # Скачиваем 10 последних постов
    post_count = 0
    for post in profile.get_posts():
        if post_count >= 7:
            break

        if not post.is_video:
            # Скачиваем пост
            loader.download_post(post, target=target_username)
            post_count += 1

            # Получаем список скачанных файлов для этого поста
            post_files = [
                f for f in os.listdir(target_username) if f.startswith(post.shortcode)
            ]

            # Переименовываем файлы
            for i, filename in enumerate(post_files):
                ext = os.path.splitext(filename)[1]
                new_name = f"{target_username}_{post_count}_{i + 1}{ext}"
                old_path = os.path.join(target_username, filename)
                new_path = os.path.join(target_username, new_name)
                os.rename(old_path, new_path)
                print(f"Переименовано: {filename} -> {new_name}")

        time.sleep(2)  # Задержка между постами

    print(
        f"\nСкачано {post_count} постов с изображениями из профиля @{target_username}"
    )


def run_instaloader_with_vpn():
    # Запускаем OpenVPN
    vpn_process = subprocess.Popen(
        [
            "openvpn",
            # "--config", os.path.join(STATIC_FILES, 'data', 'overlord.ovpn'),
            "--config",
            './static/data/overlord.ovpn',
            "--daemon",
        ]
    )

    # Ждем подключения
    time.sleep(10)

    current_ip = get_current_ip()
    print(f"Текущий IP: {current_ip}")

    try:
        # Используем Instaloader
        download_and_rename_posts()

    finally:
        # Гарантируем, что VPN завершится даже при ошибке
        vpn_process.terminate()


if __name__ == '__main__':
    download_and_rename_posts()
