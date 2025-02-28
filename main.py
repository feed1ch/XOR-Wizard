import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from userstates import UserStates
import utils
from config import TOKEN

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔐 Зашифровать текст 🔐", callback_data="encrypt")
    builder.button(text="🔓 Расшифровать текст 🔓", callback_data="decrypt")
    builder.adjust(1, 2)
    await message.answer(
        f"Добро пожаловать, {html.bold(message.from_user.full_name)}!\n\n"
        f"Воспользуйтесь кнопками ниже",
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(F.data == "encrypt")
async def encrypt_get_text(callback: CallbackQuery, state: FSMContext) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔴 Отмена 🔴", callback_data="cancel")
    await state.set_state(UserStates.encrypt_text)
    await callback.message.answer(
        "Введите исходный текст", reply_markup=builder.as_markup()
    )


@dp.message(UserStates.encrypt_text, F.text)
async def encrypt_get_text(message: Message, state: FSMContext) -> None:
    await message.delete()
    await state.update_data(text=message.text)
    builder = InlineKeyboardBuilder()
    builder.button(text="🔑 Сгенерировать ключ 🔑", callback_data="generate_key")
    builder.button(text="🔴 Отмена 🔴", callback_data="cancel")
    builder.adjust(1, 2)
    await message.answer(
        "Придумайте ключ или сгенерируйте случайный", reply_markup=builder.as_markup()
    )
    await state.set_state(UserStates.encrypt_key)


@dp.message(UserStates.encrypt_key, F.text)
async def encrypt_get_key(message: Message, state: FSMContext) -> None:
    await message.delete()
    data = await state.get_data()
    plaintext = data["text"]
    key = message.text
    encrypted_base64, encrypted_bin = utils.xor_encrypt(plaintext, key)
    if len(plaintext) > len(key):
        key = key * (len(plaintext) // len(key)) + key[: len(plaintext) % len(key)]
    await message.answer(
        f"{html.bold('Бинарное представление исходного текста')}\n\n"
        f"{html.pre_language(utils.str_to_bin(plaintext), 'bin')}"
    )
    await message.answer(
        f"{html.bold('Бинарное представление ключа')}\n\n"
        f"{html.pre_language(utils.str_to_bin(key), 'bin')}"
    )
    await message.answer(
        f"{html.bold('Бинарное представление зашифрованного текста')}\n\n"
        f"{html.pre_language(' '.join(encrypted_bin), 'bin')}"
    )
    await message.answer(
        f"{html.bold('Зашифрованный текст в Base64')}\n\n"
        f"{html.code(encrypted_base64)}"
    )
    await state.clear()


@dp.callback_query(UserStates.encrypt_key, F.data == "generate_key")
async def encrypt_generate_key(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    plaintext = data["text"]
    key = utils.generate_random_key(len(plaintext))
    encrypted_base64, encrypted_bin = utils.xor_encrypt(plaintext, key)
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑️ Удалить 🗑️", callback_data="delete_message")
    await callback.message.answer(
        f"{html.bold('Бинарное представление исходного текста')}\n\n"
        f"{html.pre_language(utils.str_to_bin(plaintext), 'bin')}"
    )
    await callback.message.answer(
        f"{html.bold('Бинарное представление ключа')}\n\n"
        f"{html.pre_language(utils.str_to_bin(key), 'bin')}"
    )
    await callback.message.answer(
        f"{html.bold('Бинарное представление зашифрованного текста')}\n\n"
        f"{html.pre_language(' '.join(encrypted_bin), 'bin')}"
    )
    await callback.message.answer(
        f"{html.bold('Зашифрованный  в Base64')}\n\n" f"{html.code(encrypted_base64)}"
    )
    await callback.message.answer(
        f"{html.bold('Ключ')}\n\n" f"{html.code(key)}", reply_markup=builder.as_markup()
    )
    await state.clear()


@dp.callback_query(F.data == "decrypt")
async def decrypt_get_text(callback: CallbackQuery, state: FSMContext) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔴 Отмена 🔴", callback_data="cancel")
    await state.set_state(UserStates.decrypt_text)
    await callback.message.answer(
        "Введите исходный текст для расшифровки", reply_markup=builder.as_markup()
    )


@dp.message(UserStates.decrypt_text, F.text)
async def decrypt_get_key(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    builder = InlineKeyboardBuilder()
    builder.button(text="🔴 Отмена 🔴", callback_data="cancel")
    await message.answer("Введите ключ", reply_markup=builder.as_markup())
    await state.set_state(UserStates.decrypt_key)


@dp.message(UserStates.decrypt_key, F.text)
async def decrypt_get_key(message: Message, state: FSMContext) -> None:
    await message.delete()
    data = await state.get_data()
    plaintext = data["text"]
    key = message.text
    try:
        decrypted_message = utils.xor_decrypt(plaintext, key)
        await message.answer(
            f"{html.bold('Расшифрованный текст')}\n\n" f"{html.code(decrypted_message)}"
        )
    except Exception as e:
        logger.error(f"Ошибка при дешифровании: {e}")
        await message.answer("⚠️ Произошла ошибка, проверьте правильность данных")
    await state.clear()


@dp.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Действие отменено")
    await state.clear()


@dp.callback_query(F.data == "delete_message")
async def delete(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await callback.message.delete()
    await state.clear()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
