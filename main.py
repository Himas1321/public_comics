import os
import random
import requests
from dotenv import load_dotenv
import telegram


def fetch_random_comic():
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    last_comic_num = response.json()["num"]

    random_comic_num = random.randint(1, last_comic_num)

    response = requests.get(f"https://xkcd.com/{random_comic_num}/info.0.json")
    response.raise_for_status()
    comic = response.json()

    img_url = comic["img"]
    alt_text = comic["alt"]

    return img_url, alt_text


def download_comic(url):
    response = requests.get(url)
    response.raise_for_status()

    filename = "comic.png"

    with open(filename, "wb") as file:
        file.write(response.content)

    return filename


def send_to_telegram(bot, chat_id, filename, caption):
    with open(filename, "rb") as photo:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption
        )


def main():
    load_dotenv()

    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    bot = telegram.Bot(token=telegram_token)

    img_url, caption = fetch_random_comic()
    filename = download_comic(img_url)

    try:
        send_to_telegram(bot, chat_id, filename, caption)
    finally:
        os.remove(filename)


if __name__ == "__main__":
    main()