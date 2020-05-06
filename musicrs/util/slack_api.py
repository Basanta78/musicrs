"""
Slack API utility
"""
import os
import json
import slack
import musicrs.settings as settings
from musicrs.util.date_time import *

from musicrs.model.base import UserProfile
from musicrs.model.db_session import session_scope
from musicrs.util.youtube import get_video_id, generate_url
from musicrs.util.numpy import serialize
from musicrs.recommendation_engine.inference import generate_inference

SLACK_API_TOKEN = settings.SLACK_API_TOKEN
SLACK_BOT_TOKEN = settings.SLACK_BOT_TOKEN
slackClient = slack.WebClient(token=SLACK_API_TOKEN)
slackBotClient = slack.WebClient(token=SLACK_BOT_TOKEN)


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

    oldest = date_to_timestamp(start_date)
    latest = date_to_timestamp(end_date)

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


def post_slack_message(user_id, video_id):
    try:
        dm_response = slackBotClient.conversations_open(users=user_id)
        dm_channel = dm_response["channel"]["id"]
        video_url = generate_url(video_id=video_id)

        response = slackBotClient.chat_postMessage(
            channel=dm_channel,
            text=video_url
        )
        print("Posted {0} to the user {1}".format(video_url, user_id))
    except:
        print("Cannot post video to the user: " + str(user_id))


def dump_slack_to_db(slack_message, serialized_np):
    """
    Dump slack youtube urls and user profile to db
    :param slack_message: dict
    :param serialized_np: str
    """
    video_id = get_video_id(slack_message["song_url"])
    with session_scope() as session:
        identity = (
            session.query(UserProfile)
            .filter_by(user_id=slack_message["user"], video_id=video_id)
            .first()
        )

        if not identity:
            user_profile = UserProfile(
                user_id=slack_message["user"],
                user_name=slack_message["user_real_name"],
                user_email=slack_message["user_email"],
                user_profile_picture=slack_message["user_profile_picture"],
                video_id=video_id,
                audio_encoding=serialized_np,
            )
            session.add(user_profile)


def load_slack_messages(start_date, end_date):
    """
    Retrieve slack messages and encoding and load into db
    :param start_date: str (YYYY-mm-dd)
    :param end_date: str (YYYY-mm-dd)
    """
    slack_channel = settings.SLACK_CHANNEL_ID
    retrieved_messages = retrieve_slack_messages(channel, start_date, end_date)
    for slack_message in retrieved_messages:
        inference = generate_inference(slack_message["song_url"])
        serialized_np = serialize(inference)
        dump_slack_to_db(slack_message, serialized_np)
