import os, json, platform, sys, traceback
from zipfile import ZipFile

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

	print("\n\033[95m\033[1mMinecraft Version Unpacker v1.1.0\n(C) 2021 by Nineteendo\033[0m\n")
	print("Working directory: " + os.getcwd())
	try:
		update_json(options, json.load(open(os.path.join(sys.path[0], "options.json"), "rb")))
	except Exception as e:
		error_message("%s in options.json: %s" % (type(e).__name__, e))
		
	if platform.system() in options["minecraftFolder"]:
		path = os.path.expanduser(options["minecraftFolder"][platform.system()])
	else:
		raise SystemError("Unknown system: %s" % platform.system())

	version = input("\033[1mVersion=\033[0m ")
	try:
		version_id = json.load(open(os.path.join(path, "versions/%s/%s.json" % (version, version)), "rb"))["id"]
		pathout = input("\033[1mOutput directory\033[0m: ")
		with ZipFile(os.path.join(path, "versions/%s/%s.jar" % (version_id, version_id)), 'r') as zipObj:
			for fileName in zipObj.namelist():
				if not fileName.endswith(options["ignoreExtensions"]):
					zipObj.extract(fileName, pathout)
					print("wrote " + fileName)
	except Exception:
		error_message(version + " not found")
	
except BaseException as e:
	error_message('%s: %s' % (type(e).__name__, e))
fail.close()
