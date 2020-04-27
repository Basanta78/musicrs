import os

def delete_all_files(basePath):
  fileLists = os.listdir(basePath)
  for fileName in fileLists:
    delete_file(basePath,fileName)

def delete_file(basePath,fileName):
  filePath = os.path.join(basePath, fileName)
  os.remove(filePath)