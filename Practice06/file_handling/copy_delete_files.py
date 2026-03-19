import shutil
shutil.copy("sample.txt", "backup.txt")


import os
if os.path.exists("backup.txt"):
    os.remove("backup.txt")
else:
    print("no such file")