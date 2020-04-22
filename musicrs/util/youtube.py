""" YoutubeDL utility """

from __future__ import unicode_literals
import os
import youtube_dl


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
