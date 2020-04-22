import os

from musicrs.util.audioTrimmer import audioTrimmer
from musicrs.util.youtube import download_from_youtube, generate_url
from musicrs.recommendation_engine.mxnet_audio.library.cifar10 import (
    Cifar10AudioClassifier,
)
from musicrs.model.db_session import session_scope
from musicrs.model.base import Inference
from musicrs.util.numpy import serialize


def process_url(url):
    """
    Process youtube url
    :param url: youtube url
    :return: processed file path
    """
    download_path = "/tmp/"
    output_format = "wav"
    file_path = download_from_youtube(url, output_format, download_path)
    trimmed_file_path = audioTrimmer(
        file_path, output_format, startMin=0, startSec=0, endMin=0, endSec=30
    )
    return trimmed_file_path


def dump_inteference_db(video_id, serialized_np):
    """
    Dump generated numpy array in db
    :param url: video url
    :param serialized_np: serialized numpy array
    """
    with session_scope() as session:
        identity = session.query(Inference).filter_by(video_id=video_id).first()
        if not identity:
            inference = Inference(video_id=video_id, audio_encoding=serialized_np)
            session.add(inference)


def check_new_video(video_id):
    """
    Check if the video id is new
    :param video_id: video id
    :return: bool
    """
    with session_scope() as session:
        identity = session.query(Inference).filter_by(video_id=video_id).first()
        if identity:
            return True
        return False


def generate_inference(url):
    """
    Generate inference encoding from the url
    :param url: youtube url
    :return: numpy array
    """
    audio_path = process_url(url)
    classifier = Cifar10AudioClassifier()
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_path, "demo/models/")
    classifier.load_model(model_dir_path=model_path)
    np_array = classifier.encode_audio(audio_path)
    return np_array


def read_training_file(file_path):
    """
    Read training file
    :param file_path: file path
    :return: video id list
    """
    video_id_list = []
    with open(file_path) as fp:
        for video_id in fp:
            processed_id = video_id.strip()
            if processed_id != "" and "#" not in processed_id:
                video_id_list.append(processed_id)
        return video_id_list


def load_inference(file_path):
    """
    Load inferences to database table
    """
    # Read training files
    video_ids = read_training_file(file_path)
    for video_id in video_ids:
        if check_new_video(video_id):
            continue
        url = generate_url(video_id)
        np_array = generate_inference(url)
        serialized_np = serialize(np_array)
        dump_inteference_db(video_id, serialized_np)
    # delete audio and video files
