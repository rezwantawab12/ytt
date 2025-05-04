import yt_dlp
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

api_key = "7801225750:AAEqJnAvQgGI7pXXKemNkW3yp4qrdz1JOIU"
bot = telebot.TeleBot(api_key)

# دکمه‌های کیفیت
butt = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
butt.add("144p", "240p", "360p", "720p", "1080p")

uurl = {}  # ذخیره لینک هر کاربر
valid_qualities = ["144p", "240p", "360p", "720p", "1080p"]

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "به ربات دانلود یوتیوب خوش آمدید!\nلطفاً لینک ویدیوی یوتیوب را بفرستید.")

@bot.message_handler()
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()
    print(text)

    # مرحله 1: کاربر لینک فرستاده
    if "youtube.com" in text or "youtu.be" in text:
        uurl[chat_id] = {"url": text}
        bot.send_message(chat_id, "لطفاً کیفیت مورد نظر را انتخاب کنید:", reply_markup=butt)

    # مرحله 2: کاربر کیفیت را فرستاده
    elif text in valid_qualities and chat_id in uurl:
        url = uurl[chat_id]["url"]
        q = text.replace("p", "")  # حذف p برای استفاده در فیلتر

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': f'best[height<={q}]',
            'noplaylist': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                direct_link = info['url']

                button = InlineKeyboardButton(text="دانلود", url=direct_link)
                markup = InlineKeyboardMarkup().add(button)

                bot.send_message(chat_id, "لینک دانلود شما آماده است:", reply_markup=markup)
                del uurl[chat_id]  # پاک کردن داده برای استفاده بعدی
        except Exception as e:
            bot.send_message(chat_id, "خطا در پردازش:")

    # ورودی نامعتبر
    else:
        bot.send_message(chat_id, "لطفاً ابتدا یک لینک یوتیوب ارسال کنید.")

bot.polling(skip_pending=True)