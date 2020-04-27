""" YoutubeDL utility """

from __future__ import unicode_literals
import os
import youtube_dl
import re


def download_from_youtube(video_link: str, output_format: str, download_path: str):
    """
    Download video/audio from youtube link
    :param video_link: youtube link
    :param output_format: output format
    :param download_path: download path
    """
    params = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": output_format,
                "preferredquality": "192",
            }
        ],
        "postprocessor_args": ["-ar", "16000"],
        "prefer_ffmpeg": False,
        "keepvideo": False,
        "outtmpl": "{}%(title)s.%(ext)s".format(download_path),
        "noplaylist": True,
        "extractaudio": True,
    }
    with youtube_dl.YoutubeDL(params) as ydl:
        info = ydl.extract_info(video_link, download=True)
        file_name = "{}.{}".format(info["title"], output_format)
        file_path = os.path.join(download_path, file_name)
        return file_path


def get_video_id(youtube_url):
    """
    Get video id from youtube url
    :param youtube_url: youtube url
    :return: video id
    """
    regex = re.compile(
        r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})"
    )

    match = regex.match(youtube_url)

    return match.group("id")


def generate_url(video_id):
    """
    Get youtube url link from video id
    :param video_id: video id
    :return: youtube url
    """
    base_url = "https://www.youtube.com/watch?v="
    return base_url + video_id
