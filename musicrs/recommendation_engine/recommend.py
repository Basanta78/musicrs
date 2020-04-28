import numpy as np
from musicrs.util.numpy import de_serialize
from musicrs.recommendation_engine.inference import fetch_inference_db
from musicrs.recommendation_engine.similarity import index_database_vector, search


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


def recommend_music():
    """
    Recommend music based on similarity
    """
    # fetch user data
    data = fetch_inference_db()
    encoding_list = get_encoding_list(data)
    index = index_database_vector(len(encoding_list[0]), encoding_list)
    search(index, encoding_list, 1)


recommend_music()
