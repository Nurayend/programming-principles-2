#файлы в заданной папке
import os
# entries = os.listdir()

# for entry in entries:
#   print(entry)
# ----------------------
with os.scandir("/Users/MI/Desktop") as entries:
  for entry in entries:
    entry.name
os.path.isfile
os.path.join

basepath = "/Users/MI/Desktop"
for entry in os.listdir(basepath):
  if os.path.isfile(os.path.join(basepath, entry)):
    entry