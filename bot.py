from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile,
)
from downloader import download_video
import asyncio
import os

# ==========================
TOKEN="8639003033:AAEsWrrhb89ubCylJhnk3H1frhqyyXa0F2c"
# ==========================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ========= START =========
@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎵 Audio",
                    callback_data="audio"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="👤 Profile",
                    callback_data="profile"
                ),
                InlineKeyboardButton(
                    text="⚙️ Settings",
                    callback_data="settings"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❓ Help",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    text="ℹ️ About",
                    callback_data="about"
                ),
            ],
        ]
    )

    await message.answer(
        "👋 Welcome to *All In One Bot!*\n\n"
        "📥 Just send me a YouTube, TikTok, Instagram, Facebook or X link and I'll download it automatically.",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )

# ========= AUDIO =========
@dp.callback_query(F.data == "audio")
async def audio(callback: CallbackQuery):
    await callback.message.answer(
        "🎵 Audio conversion is coming soon."
    )
    await callback.answer()

# ========= PROFILE =========
@dp.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user = callback.from_user

    await callback.message.answer(
        f"👤 Profile\n\n"
        f"Name: {user.full_name}\n"
        f"Username: @{user.username}\n"
        f"ID: {user.id}"
    )

    await callback.answer()

# ========= SETTINGS =========
@dp.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery):
    await callback.message.answer(
        "⚙️ Settings will be available soon."
    )
    await callback.answer()

# ========= HELP =========
@dp.callback_query(F.data == "help")
async def help(callback: CallbackQuery):
    await callback.message.answer(
        "📖 Just paste a supported video link.\n\n"
        "Supported:\n"
        "• YouTube\n"
        "• TikTok\n"
        "• Instagram\n"
        "• Facebook\n"
        "• X (Twitter)"
    )
    await callback.answer()

# ========= ABOUT =========
@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.message.answer(
        "🤖 All In One Bot\n\n"
        "Version 1.0\n"
        "Developed with Python & Aiogram."
    )
    await callback.answer()

# ========= RECEIVE LINK =========
@dp.message()
async def receive_link(message: Message):

    if not message.text:
        return

    url = message.text.strip()

    supported = [
        "youtube.com",
        "youtu.be",
        "tiktok.com",
        "vt.tiktok.com",
        "vm.tiktok.com",
        "instagram.com",
        "facebook.com",
        "fb.watch",
        "x.com",
        "twitter.com",
    ]

    if not any(site in url for site in supported):
        return

    wait = await message.answer("⏳ Downloading...")

    try:
        file_path = download_video(url)

        video = FSInputFile(file_path)

        await message.answer_video(
            video=video,
            caption="✅ Download complete!"
        )

        await wait.delete()

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await wait.edit_text(
            f"❌ Download failed.\n\n{e}"
        )

# ========= RUN =========
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())