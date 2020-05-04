from musicrs.util.object import as_dict
from musicrs.model.base import Recommendation
from musicrs.model.db_session import session_scope


def dump_user_recommendation(user_id, url, similarity):
    """
    Dump user recommendation info
    :param user_id: user id
    :param url: recommended url
    :param similarity: similarity percentage
    """
    with session_scope() as session:
        user = session.query(Recommendation).filter_by(user_id=user_id, recommended_url=url).first()
        if not user:
            user_recommend = Recommendation(user_id=user_id, recommended_url=url, similarity=similarity)
            session.add(user_recommend)


def fetch_user_recommendation(user_id):
    """
    Fetch user recommendation
    :param user_id: user id
    """
    user_data = []
    with session_scope() as session:
        data = session.query(Recommendation).filter_by(user_id=user_id).all()
        for d in data:
            user_data.append(as_dict(d))
    return user_data
