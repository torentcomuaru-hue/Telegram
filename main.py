import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMINS = [7947791483, 7200257195]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

WELCOME_TEXT = (
    "👋 Приветствую!\n\n"
    "🔥 Вип доступ к эксклюзивному контенту:\n\n"
    "[Vip] Sissy – 1500₽\n"
    "[Vip] Femdom – 1500₽\n"
    "[Vip] Russian joi & cei – 1500₽\n"
    "[Vip] Трансы – 1500₽\n"
    "[Vip] Куколды – 1000₽\n\n"
    "✅ Все цены указаны *навсегда*\n"
    "🎁 Покупка нескольких ВИП — скидка!\n\n"
    "💳 Оплата возможна:\n"
    "— в любой валюте, с любой карты, из любой страны\n"
    "— криптовалюта\n"
    "— скины CS:GO / Dota\n\n"
    "✍️ Напишите, что вы выбрали, и администратор свяжется с вами."
)

admin_msg_to_user = {}

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(WELCOME_TEXT, parse_mode="Markdown")
    for admin_id in ADMINS:
        await bot.send_message(admin_id,
            f"🔔 Новый клиент @{message.from_user.username or message.from_user.full_name} "
            f"(ID: {message.from_user.id}) нажал /start"
        )

@dp.message()
async def all_messages_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        if message.reply_to_message:
            original_msg_id = message.reply_to_message.message_id
            if original_msg_id in admin_msg_to_user:
                user_id = admin_msg_to_user[original_msg_id]
                await bot.send_message(user_id, message.text)
                await message.answer("✅ Ответ отправлен клиенту")
            else:
                await message.answer("⚠️ Невозможно определить клиента. Ответьте на сообщение клиента.")
        else:
            await message.answer("⚠️ Чтобы ответить, нажмите 'Ответить' на сообщение клиента.")
    else:
        for admin_id in ADMINS:
            msg = await bot.send_message(admin_id,
                f"📩 Сообщение от @{message.from_user.username or message.from_user.full_name} "
                f"(ID: {message.from_user.id}):\n\n{message.text}"
            )
            admin_msg_to_user[msg.message_id] = message.from_user.id

async def main():
    print("Запускаем бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
