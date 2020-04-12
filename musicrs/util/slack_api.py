"""
Slack API utility
"""
import os
import json
import slack
import musicrs.settings as settings

SLACK_API_TOKEN = settings.SLACK_API_TOKEN
slackClient = slack.WebClient(token=SLACK_API_TOKEN)


def retrieve_slack_messages(channel: str):
    """
    Retrieve youtube links from slack channel
    :param channel: Slack channel id
    :type channel: string
    :return slack channel messages
    :rtype list
    """
    response = slackClient.conversations_history(channel=channel)
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
