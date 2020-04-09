"""
Slack API utility
"""
import os
import json
import slack

SLACK_TOKEN = ""
slackClient = slack.WebClient(token=SLACK_TOKEN)


def retrieve_slack_messages(channel: str):
    """
    Retrieve youtube links from slack channel
    """
    response = slackClient.conversations_history(channel=channel)
    messages = response["messages"]
    for m in messages:
        pass