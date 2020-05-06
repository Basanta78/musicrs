import numpy as np
from musicrs.util.numpy import de_serialize
from musicrs.util.youtube import generate_url
from musicrs.recommendation_engine.inference import fetch_inference_db
from musicrs.recommendation_engine.user_profile import fetch_user_profile
from musicrs.recommendation_engine.similarity import (
    index_database_vector,
    search,
    get_max_similarity,
)
from musicrs.recommendation_engine.user_recommend import dump_user_recommendation


def get_encoding_list(data):
    """
    Process the encodings
    :param data:  encoding
    :return: numpy array of encodings
    """
    encodings = []
    for d in data:
        encodings.append(de_serialize(d["audio_encoding"]).astype("float32"))
    return np.asarray(encodings)


def recommend_music(user_id):
    """
    Recommend music based on similarity
    """
    # fetch user data
    user_data = fetch_user_profile(user_id)
    inference_data = fetch_inference_db()
    user_encoding = get_encoding_list(user_data)
    inference_encoding = get_encoding_list(inference_data)
    index = index_database_vector(len(inference_encoding[0]), inference_encoding)
    similarity_list = search(index, user_encoding, 1)
    most_similar = get_max_similarity(similarity_list)
    similar_encoding = inference_data[most_similar[1]]
    recommend_url = generate_url(similar_encoding["video_id"])
    similarity_percent = most_similar[0] * 100
    dump_user_recommendation(user_id, recommend_url, similarity_percent)
