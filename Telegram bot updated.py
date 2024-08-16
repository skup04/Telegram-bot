from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = ''
ADMIN_ID =
CHANNEL_ID = '@'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
pending_messages = {}



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, Я телеграмм бот группы Fizfuck.Confessions\n\n Любое сообщение, написанное в бота, будет передано на рассмотрение админу")



@dp.message_handler(content_types=types.ContentTypes.ANY)
async def handle_message(message: types.Message):
    message_id = message.message_id

    # Клавиатура с кнопкой "Подтвердить"
    keyboard = InlineKeyboardMarkup()
    confirm_button = InlineKeyboardButton("Публиш", callback_data=f"approve:{message_id}")
    keyboard.add(confirm_button)


    pending_messages[message_id] = {
        'text': message.text,
        'caption': message.caption,
        'photo': message.photo[-1].file_id if message.photo else None,
        'video': message.video.file_id if message.video else None,
        'voice': message.voice.file_id if message.voice else None,
        'document': message.document.file_id if message.document else None,
        'sticker': message.sticker.file_id if message.sticker else None,
    }

    if message.text:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=message.text,
            reply_markup=keyboard
        )
    if message.photo:
        await bot.send_photo(
            chat_id=ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=message.caption,
            reply_markup=keyboard
        )
    if message.video:
        await bot.send_video(
            chat_id=ADMIN_ID,
            video=message.video.file_id,
            caption=message.caption,
            reply_markup=keyboard
        )
    if message.voice:
        await bot.send_voice(
            chat_id=ADMIN_ID,
            voice=message.voice.file_id,
            caption=message.caption,
            reply_markup=keyboard
        )
    if message.document:
        await bot.send_document(
            chat_id=ADMIN_ID,
            document=message.document.file_id,
            caption=message.caption,
            reply_markup=keyboard
        )
    if message.sticker:
        await bot.send_sticker(
            chat_id=ADMIN_ID,
            sticker=message.sticker.file_id,
            reply_markup=keyboard
        )
    await bot.send_message(chat_id=message.chat.id, text="Ваше сообщение передано!")



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('approve'))
async def process_callback(callback_query: types.CallbackQuery):
    _, message_id = callback_query.data.split(":")

    message_id = int(message_id)

    if message_id in pending_messages:
        message_info = pending_messages.pop(message_id)
        if message_info['text']:
            await bot.send_message(
                chat_id=CHANNEL_ID, text=message_info['text']
            )
        if message_info['photo']:
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=message_info['photo'],
                caption=message_info['caption']
            )
        if message_info['video']:
            await bot.send_video(
                chat_id=CHANNEL_ID,
                video=message_info['video'],
                caption=message_info['caption']
            )
        if message_info['voice']:
            await bot.send_voice(
                chat_id=CHANNEL_ID,
                voice=message_info['voice'],
                caption=message_info['caption']
            )
        if message_info['document']:
            await bot.send_document(
                chat_id=CHANNEL_ID,
                document=message_info['document'],
                caption=message_info['caption']
            )
        if message_info['sticker']:
            await bot.send_sticker(
                chat_id=CHANNEL_ID,
                sticker=message_info['sticker']
            )
        await callback_query.answer("Сообщение опубликовано в канале.")
    else:
        await callback_query.answer("Сообщение не найдено или уже было обработано.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
