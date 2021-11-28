import os, shutil, json, platform, sys

try:
	if sys.version_info[0] < 3:
		raise RuntimeError("Must be using Python 3")

	print("\n\033[95m\033[1mMinecraft Asset Unpacker v1.1.0\n(C) 2021 by Nineteendo\033[0m\n")
	if (platform.system() == "Darwin"):
		path = os.path.expanduser('~/Library/Application Support/minecraft/assets/')
	elif (platform.system() == "Linux"):
		path = os.path.expanduser('~/.minecraft/assets/')
	elif (platform.system() == "Windows"):
		path = os.path.expandvars('%APPDATA%\.minecraft/assets/')
	else:
		print("Unknown system: %s" % platform.system())

	print("\033[1mOptions:\033[0m " + " ".join(sorted(os.listdir(path + "indexes/"))).replace(".json",""))
	version = input("\033[1mVersion=\033[0m ")
	data = json.loads(open(path + "indexes/" + version + ".json",'r').read())["objects"]
	for location in data:
		print("wrote " + version + "/" + location)
		if not os.path.isdir(location):
			os.makedirs(os.path.dirname(path + version + "/" + location), exist_ok=True)
		
		hash = data[location]["hash"]
		shutil.copyfile(path + "objects/" + hash[:2] + "/" + hash, path + version + "/" + location)
	
	input("\nFinished. Press Enter\n")
except BaseException as e:
	print('\n\33[91m%s: %s\33[0m' % (type(e).__name__, e))
