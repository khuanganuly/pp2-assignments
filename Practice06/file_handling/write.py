with open("sample.txt", "w") as f:
    f.write("writing sample data")

with open("sample.txt", "a") as f:
    f.write("\nappend some new line")

with open("sample.txt", "r") as f:
    print(f.read())