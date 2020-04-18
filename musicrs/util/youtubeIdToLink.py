import os

def youtubeIdToLink(basePath):

  baseUrl = 'https://www.youtube.com/watch?v='

  entries = os.listdir(basePath)
  for entry in entries:
    f=open(os.path.join(basePath,entry), "r")
    if f.mode == 'r':
      contents =f.readlines()
      for youtubeId in contents: 
        if not '# new artist:' in youtubeId: 
          print(baseUrl+youtubeId)