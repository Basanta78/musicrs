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


def get_user_info(user_id):
    """
    Retrieve slack user info from user id
    :param user_id: slack id of the user
    :type user_id: string
    """
    response = slackClient.users_info(user=user_id)
    profile = response["user"]["profile"]
    user_info = {
        "user_display_name": profile["display_name"],
        "user_real_name": profile["real_name"],
        "user_email": profile["email"],
        "user_profile_picture": profile["image_512"],
    }

    return user_info


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

    oldest = date_to_timestamp(str(start_date))
    latest = date_to_timestamp(str(end_date))

    response = slackClient.conversations_history(
        channel=channel, latest=str(latest), oldest=str(oldest)
    )
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
                    "song_url": attached_song["original_url"],
                    "youtube_channel": attached_song["author_name"],
                }

                retrieved_message.update(song)
                retrieved_message.update(get_user_info(message["user"]))
                retrieved_messages.append(retrieved_message)

    return retrieved_messages
