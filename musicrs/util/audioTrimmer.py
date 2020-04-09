from pydub import AudioSegment
import sys
sys.path.append('/usr/bin/ffmpeg')

def audioTrimmer(files_path,file_name,fileType,startMin,startSec,endMin,endSec):

  # Time to miliseconds
  startTime = startMin*60*1000+startSec*1000
  endTime = endMin*60*1000+endSec*1000

  # Opening file and extracting segment
  segment = AudioSegment.from_file( files_path+'/'+file_name, fileType )
  extract = segment[startTime:endTime]

  # Saving
  extract.export( files_path+'/'+file_name+'-extract.mp3', format=fileType)