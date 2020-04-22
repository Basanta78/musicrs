from pydub import AudioSegment
import sys

sys.path.append("/usr/bin/ffmpeg")


def audioTrimmer(files_path, fileType, startMin, startSec, endMin, endSec):
    MIN = 60
    MILI_SECOND = 1000

    # Time to miliseconds
    startTime = startMin * MIN * MILI_SECOND + startSec * MILI_SECOND
    endTime = endMin * MIN * MILI_SECOND + endSec * MILI_SECOND

    # Opening file and extracting segment
    segment = AudioSegment.from_file(files_path, fileType)
    extract = segment[startTime:endTime]

    # Saving

    file_path = extract.export(files_path + "-extract." + fileType, format=fileType)

    return file_path.name
