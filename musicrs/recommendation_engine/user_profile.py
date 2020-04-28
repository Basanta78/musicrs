import musicrs.settings as settings
from musicrs.util.object import as_dict
from musicrs.util.numpy import serialize
from musicrs.model.base import UserProfile
from musicrs.util.youtube import get_video_id
from musicrs.model.db_session import session_scope
from musicrs.util.slack_api import retrieve_slack_messages
from musicrs.recommendation_engine.inference import generate_inference


def fetch_user_profile(user_id):
    """
    Fetch user data based on user id
    :param user_id: user id
    :return: list of user data
    """
    user_data = []
    with session_scope() as session:
        data = session.query(UserProfile).filter_by(user_id=user_id).all()
        for d in data:
            user_data.append(as_dict(d))
    return user_data


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
    retrieved_messages = retrieve_slack_messages(slack_channel, start_date, end_date)
    for slack_message in retrieved_messages:
        inference = generate_inference(slack_message["song_url"])
        serialized_np = serialize(inference)
        dump_slack_to_db(slack_message, serialized_np)
