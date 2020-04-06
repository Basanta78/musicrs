from pydub import AudioSegment
import sys
sys.path.append('/usr/bin/ffmpeg')

def audioTrimmer(file_name,startMin,startSec,endMin,endSec):
  files_path = 'mp3/'

  # Time to miliseconds
  startTime = startMin*60*1000+startSec*1000
  endTime = endMin*60*1000+endSec*1000

  # Opening file and extracting segment
  song = AudioSegment.from_mp3( files_path+file_name+'.mp3' )
  extract = song[startTime:endTime]

  # Saving
  extract.export( files_path+file_name+'-extract.mp3', format="mp3")