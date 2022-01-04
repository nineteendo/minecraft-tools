import os, shutil, json, platform, sys, traceback

options = {
	"DEBUG_MODE": False,
	"ignoreExtensions": (
		".class",
	),
	"minecraftFolder": {
		"Darwin": "~/Library/Application Support/minecraft",
		"Linux": "~/.minecraft",
		"Windows": "%APPDATA%/.minecraft"
	}
}

print(options)
def update_json(old_json, new_json):
	for key in new_json:
		if not key in old_json:
			old_json[key] = new_json[key]
		elif type(old_json[key]) == type(new_json[key]):
			if isinstance(new_json[key], dict):
				update_json(old_json[key], new_json[key])
			else:
				old_json[key] = new_json[key]
		elif isinstance(old_json[key], tuple) and isinstance(new_json[key], list):
			old_json[key] = tuple([str(i) for i in new_json[key]])

def error_message(string):
	if options["DEBUG_MODE"]:
		string = traceback.format_exc()
	
	fail.write(string + "\n")
	print("\33[91m%s\33[0m" % string)

try:
	fail = open("fail.txt", "w")
	if sys.version_info[0] < 3:
		raise RuntimeError("Must be using Python 3")

	print("\n\033[95m\033[1mMinecraft Asset Unpacker v1.1.0\n(C) 2021 by Nineteendo\033[0m\n")
	print("Working directory: " + os.getcwd())
	try:
		update_json(options, json.load(open(os.path.join(sys.path[0], "options.json"), "rb")))
	except Exception as e:
		error_message("%s in options.json: %s" % (type(e).__name__, e))
		
	if platform.system() in options["minecraftFolder"]:
		path = os.path.join(os.path.expanduser(options["minecraftFolder"][platform.system()]), "assets")
	else:
		raise SystemError("Unknown system: %s" % platform.system())

	print("\033[1mOptions:\033[0m " + " ".join(sorted(os.listdir(os.path.join(path, "indexes")))).replace(".json", ""))
	version = input("\033[1mVersion=\033[0m ")
	pathout = input("\033[1mOutput directory\033[0m: ")
	data = json.load(open(os.path.join(path, "indexes", version + ".json"),'r'))["objects"]
	for location in data:
		if not location.endswith(options["ignoreExtensions"]):
			os.makedirs(os.path.dirname(os.path.join(pathout, location)), exist_ok=True)
			file_hash = data[location]["hash"]
			try:
				shutil.copyfile(os.path.join(path, "objects", file_hash[:2], file_hash), os.path.join(pathout, location))
				print("wrote " + location)
			except:
				error_message("Missing " + file_hash)
except BaseException as e:
	error_message('%s: %s' % (type(e).__name__, e))
fail.close()
