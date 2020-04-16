"""
Slack API utility
"""
import os
import json
import slack
import musicrs.settings as settings
from musicrs.util.date_time import *

SLACK_API_TOKEN = settings.SLACK_API_TOKEN
slackClient = slack.WebClient(token=SLACK_API_TOKEN)


def retrieve_slack_messages(channel: str, start_date: str, end_date: str):
    """
    Retrieve youtube links from slack channel
    :param channel: Slack channel id
    :type channel: string
    :param start_date: str (YYYY-mm-dd)
    :param end_date: str (YYYY-mm-dd)
    :return slack channel messages
    :rtype list
    """

    oldest = date_to_timestamp(start_date)
    latest = date_to_timestamp(end_date)

    response = slackClient.conversations_history(channel=channel, latest=str(latest), oldest=str(oldest))
    retrieved_messages = []

    for message in response["messages"]:
        retrieved_message = {}

        if message["type"] == "message":
            retrieved_message["user"] = message["user"]
            retrieved_message["timestamp"] = message["ts"]

            if message.get("attachments"):
                attached_song = message["attachments"][0]
                song = {
                    "song_title": attached_song["title"],
                    "song_author": attached_song["author_name"],
                    "song_url": attached_song["original_url"],
                }

                retrieved_message.update(song)
                retrieved_messages.append(retrieved_message)

    return retrieved_messages
