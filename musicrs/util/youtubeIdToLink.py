import os

def youtube_id_to_link(basePath):
  fileLists = os.listdir(basePath)
  for fileName in fileLists:
    read_file_convert(basePath,fileName)

def read_file_convert(basePath,fileName):
  baseUrl = 'https://www.youtube.com/watch?v='

  f=open(os.path.join(basePath,fileName), "r")
  if f.mode == 'r':
    contents =f.readlines()
    for youtubeId in contents: 
      if not '#' in youtubeId: 
        print(baseUrl+youtubeId)