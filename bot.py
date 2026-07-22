from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile,
)
from downloader import download_video, download_audio
import asyncio
import os

# ==========================
TOKEN = "8639003033:AAEsWrrhb89ubCylJhnk3H1frhqyyXa0F2c"
# ==========================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Store users waiting for audio links
audio_mode = set()

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
        "📥 Send any YouTube, TikTok, Instagram, Facebook or X link.\n\n"
        "🎬 Send normally for video.\n"
        "🎵 Tap Audio first to download MP3.",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )

# ========= AUDIO =========
@dp.callback_query(F.data == "audio")
async def audio(callback: CallbackQuery):
    audio_mode.add(callback.from_user.id)

    await callback.message.answer(
        "🎵 Send the video link you want as MP3."
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
        "⚙️ Settings coming soon."
    )
    await callback.answer()

# ========= HELP =========
@dp.callback_query(F.data == "help")
async def help(callback: CallbackQuery):
    await callback.message.answer(
        "📖 Supported websites:\n\n"
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
        "🤖 All In One Bot\nVersion 1.1"
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

    # ---------- AUDIO ----------
    if message.from_user.id in audio_mode:

        audio_mode.remove(message.from_user.id)

        wait = await message.answer("🎵 Downloading audio...")

        try:
            file_path = download_audio(url)

            audio = FSInputFile(file_path)

            await message.answer_audio(
                audio=audio,
                caption="✅ MP3 Download Complete!"
            )

            await wait.delete()

            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:
            await wait.edit_text(f"❌ {e}")

        return

    # ---------- VIDEO ----------
    wait = await message.answer("⏳ Downloading video...")

    try:
        file_path = download_video(url)

        video = FSInputFile(file_path)

        await message.answer_video(
            video=video,
            caption="✅ Download Complete!"
        )

        await wait.delete()

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await wait.edit_text(f"❌ {e}")

# ========= RUN =========
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
