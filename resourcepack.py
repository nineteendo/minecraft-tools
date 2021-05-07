import os, shutil
version = input("Version=")
for line in open("indexes/"+version+".json",'r').readline().replace("}","{").split("{"):
    if "." in line:
        location=version + "/"+ line.strip('":, ')
        if not os.path.isdir(location):
            os.makedirs(os.path.dirname(location), exist_ok=True)
    if "hash" in line:
        hash = line.split(":")[1].split(",")[0].strip('" ')
        print(location)
        shutil.copyfile("objects/"+hash[:2]+"/"+hash, location)
