import os

def delete_all_files(basePath,pathfile):
  fileLists = os.listdir(basePath)
  for fileName in fileLists:
    delete_file(fileName)

def delete_file(fileName):
  os.remove(fileName)