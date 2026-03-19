import shutil

shutil.move("example.txt", "create/nested/directories/example.txt")

shutil.copy("create/nested/directories/example.txt", "copy_example.txt")