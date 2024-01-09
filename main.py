from pyrogram import Client, filters
import datetime
import pytz
from utils import db
from decouple import config

api_id = config('API_ID', cast=int)
api_hash = config('API_HASH', cast=str)

app = Client("my_account", api_id, api_hash)


def get_time():
    qti = ""
    ir = pytz.timezone("Asia/Tehran")
    qtime = datetime.datetime.now(ir).strftime("%H:%M")

    q = {'0': '０', '1': '１', '2': '２', '3': '３', '4': '４', '5': '５', '6': '６', '7': '７', '8': '８', '9': '９', ':': ':',
         ' ': ' '}
    for x in qtime:
        qti += q[str(x)]
    return qti


@app.on_message(filters.group)
async def inspect_words(client, message):
    text = message.text
    text_p = ""
    for word in db.words():
        if word in text:
            text_p = f"""
پیام جدید 📬

👤 از طرف : {message.from_user.first_name}
📍 گروه مورد نظر : {message.chat.title}
💡 ایدی : {message.from_user.id}
🔖  یوزر نیم : @{message.from_user.username}

⏰ در ساعت : {get_time()}

📝 متن پیام :
{message.text}
"""
            await app.send_message(config('CHANNEL_ID', cast=str), text_p)


@app.on_message(filters.private)
async def private(client, message):
    text = message.text
    if message.from_user.id in db.admins():
        if text.startswith("add word"):
            word = text.replace("add word", "")

            if db.word_exists(word):
                await message.reply("**در لیست کلمات بود**")

            else:
                db.add_word(word)
                await message.reply("**به لیست کلمه ها اضافه شد**")

        elif text.startswith("remove word"):
            word = text.replace("remove word", "")

            if db.word_exists(word):
                db.remove_word(word)
                await message.reply("**از لیست کلمات حذف شد**")
            else:
                await message.reply("**در لیست کلمات نبود**")

        elif text == "words":
            text_io = "لیست کلمات شما عبارت اند از : \n"
            for i in db.words():
                text_io += f"`{i}`\n"

            await message.reply(text_io)

        elif text == "admins":
            text_io = "لیست ادمین های شما عبارت اند از : \n"
            for i in db.admins():
                text_io += f"`{i}`\n"

            await message.reply(text_io)

        elif text == "ping":
            await message.reply("ربات آنلاین است")

        elif text.startswith("add admin"):
            admin_id = text.replace("add admin", "")
            if db.admin_exists(admin_id):
                await message.reply("**در لیست ادمین ها بود**")

            else:
                db.add_admin(admin_id)
                await message.reply("**به لیست ادمیت ها اضافه شد**")

        elif text.startswith("remove admin"):
            admin_id = text.replace("remove admin", "")
            if db.admin_exists(admin_id):
                if admin_id != config('DEFAULT_ADMIN'):
                    db.remove_admin(admin_id)
                    await message.reply("**از لیست ادمین ها حذف شد**")
                else:
                    await message.reply("**شما نمیتوانید ادمین اصلی را حذف کنید**")
            else:
                await message.reply("**در لیست ادمین ها نبود**")


app.run()
