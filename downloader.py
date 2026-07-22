import yt_dlp
import os
import requests

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def expand_tiktok_url(url):
    if "vt.tiktok.com" in url or "vm.tiktok.com" in url:
        try:
            response = requests.get(url, allow_redirects=True, timeout=10)
            return response.url
        except Exception:
            return url
    return url


def clean_url(url):
    url = expand_tiktok_url(url)

    if "tiktok.com" in url:
        url = url.split("?")[0]

    return url


def download_video(url):
    url = clean_url(url)

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info)

        if not os.path.exists(filename):
            filename = os.path.splitext(filename)[0] + ".mp4"

        return filename


def download_audio(url):
    url = clean_url(url)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"

        return filename
