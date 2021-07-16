import os, shutil

print("\n\033[95m\033[1mMinecraft Asset Unpacker v1.0.0\n(C) 2021 by Nineteendo\033[0m\n")
path = os.path.expanduser('~/Library/Application Support/minecraft/assets/')

print("\033[1mOptions:\033[0m " + " ".join(sorted(os.listdir(path + "indexes/"))).replace(".json",""))
version = input("\033[1mVersion=\033[0m ")

for line in open(path + "indexes/" + version + ".json",'r').readline().replace("}", "{").split("{"):
    if "." in line:
        location=version + "/" + line.strip('":, ')
        if not os.path.isdir(location):
            os.makedirs(os.path.dirname(location), exist_ok=True)
    if "hash" in line:
        hash = line.split(":")[1].split(",")[0].strip('" ')
        print(location)
        shutil.copyfile(path + "objects/" + hash[:2] + "/" + hash, path + location)
input("\nFinished. Press Enter")
