import traceback, json, os, platform, sys, hashlib, datetime
options = {
	"allVersions": False,
	"autoNames": True,
	"customGameDir": "",
	"customGameDirForVersions": False,
	"DEBUG_MODE": False,
	"downloadVersions": False,
	"hidePlayerSafetyDisclaimer": True,
	"javaArgs": "",
	"minecraftFolder": {
		"Darwin": "~/Library/Application Support/minecraft",
		"Linux": "~/.minecraft",
		"Windows": "%APPDATA%/.minecraft"
	},
	"moddedVersions": True,
	"notPlayedVersions": True,
	"officialVersions": True,
	"old_alpha": True,
	"old_beta": True,
	"pendingVersions": True,
	"playedVersions": True,
	"releases": True,
	"resolutionHeight": 0,
	"resolutionWidth": 0,
	"snapshots": True,
	"sortBy": "releaseTime",
	"specialVersions": {},
	"stringReplace": {},
	"typeNames": {}
}

def error_message(string):
	if options["DEBUG_MODE"]:
		string = traceback.format_exc()
	
	fail.write(string + "\n")
	print("\33[91m%s\33[0m" % string)

def update_json(old_json, new_json):
	for key in new_json:
		if not key in old_json:
			old_json[key] = new_json[key]
		elif type(old_json[key]) == type(new_json[key]):
			if isinstance(new_json[key], dict):
				update_json(old_json[key], new_json[key])
			else:
				old_json[key] = new_json[key]
		
def period_name(value, version_type):
	if value in options["specialVersions"]:
		value = options["specialVersions"][value]
		
	for key in options["stringReplace"]:
		value = value.replace(key, options["stringReplace"][key])
		
	if version_type in options["typeNames"]:
		value = options["typeNames"][version_type] + " " + value
		
	return value

try:
	fail = open("fail.txt", "w")
	if sys.version_info[0] < 3:
		raise RuntimeError("Must be using Python 3")
	import urllib.request # Prevent program from crashing before version check

	if platform.system() in options["minecraftFolder"]:
		minecraft_folder = os.path.expanduser(options["minecraftFolder"][platform.system()])
	else:
		raise SystemError("Unknown system: %s" % platform.system())

	print("\033[95m\033[1mMinecraft Launcher Manager v1.1.0\n(C) 2021 by Nineteendo\033[0m\n")
	try:
		update_json(options, json.load(open(os.path.join(sys.path[0], "options.json"), "rb")))
	except Exception as e:
		error_message('%s in options.json: %s' % (type(e).__name__, e))

	open(os.path.join(minecraft_folder, "versions/version_manifest_v2.json"), "wb").write(urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json").read())
	version_manifest = json.load(open(os.path.join(minecraft_folder, "versions/version_manifest_v2.json"), "rb"))
	versions = version_manifest["versions"]
	launcher_profiles = {
		"profiles": {},
		"version" : 3
	}
	profiles = {}
	try:
		update_json(launcher_profiles, json.load(open(os.path.join(minecraft_folder, "launcher_profiles.json"), "rb")))
	except Exception as e:
		error_message('%s in launcher_profiles.json: %s' % (type(e).__name__, e))

	if options["allVersions"]:
		allIds = {}
		for path in os.listdir(minecraft_folder + "versions/"):
			try:
				version = json.load(open(os.path.join(minecraft_folder, "versions/%s/%s.json" % (path, path)), "rb"))
				allIds[version["id"]] = {
					"icon": "Furnace",
					"type": "custom"
				}
			except Exception:
				pass

		for obj in versions:
			allIds[obj["id"]] = {
				"icon": "Furnace",
				"type": "custom"
			}			

		allIds["latest-release"] = {
				"icon": "Grass",
				"type": "latest-release"
			}
		allIds["latest-snapshot"] = {
				"icon": "Crafting_Table",
				"type": "latest-snapshot"
			}
		for version_id in allIds:
			profiles[hashlib.md5(version_id.encode()).hexdigest()] = {
				"created" : datetime.datetime.now().isoformat(),
				"icon" : allIds[version_id]["icon"],
				"lastUsed" : "1970-01-02T00:00:00.000Z",
				"lastVersionId" : version_id,
				"name": "",
				"type": allIds[version_id]["type"]
			}
	else:
		profiles = launcher_profiles["profiles"]

	print("Starting to process profiles:")
	if options["hidePlayerSafetyDisclaimer"]:
		hidePlayerSafetyDisclaimer = {}

	for key in sorted(profiles, key = lambda key : profiles[key]["lastVersionId"]):
		obj = profiles[key]
		lastVersionId = obj["lastVersionId"]
		if lastVersionId == "latest-release":
			lastVersionId = version_manifest["latest"]["release"]
		elif lastVersionId == "latest-snapshot":
			lastVersionId = version_manifest["latest"]["snapshot"]
	
		version_list = list(filter(lambda version_id: version_id['id'] == lastVersionId, versions))
		if version_list != []:
			version = version_list[0]
			version_id = version["id"]
			file = minecraft_folder + "versions/%s/%s.json" % (version_id, version_id)
			if not options["downloadVersions"] and not os.path.isfile(file):
				os.makedirs(os.path.dirname(file), exist_ok=True)
				try:
					open(file, "wb").write(urllib.request.urlopen(version["url"]).read())
				except:
					error_message("Couldn't download json for " + lastVersionId)
	
		played = True
		try:
			version = json.load(open(os.path.join(minecraft_folder, "versions/%s/%s.json" % (lastVersionId, lastVersionId)), "rb"))
			version_id = version["id"]
			if not os.path.isfile(os.path.join(minecraft_folder, "versions/%s/%s.jar" % (version_id, version_id))):
				played = False
			time = datetime.datetime.fromisoformat(version["releaseTime"]).isoformat()
			version_type = version["type"]
		except Exception as e:
			played = False
			try:
				version = version_list[0]
				time = version["releaseTime"]
				version_type = version["type"]
			except Exception:
				print("Broken custom version:" + lastVersionId)
				time = "1970-01-01T00:00:00.000Z"
				version_type = ""

		if options["downloadVersions"] and not os.path.isfile(os.path.join(minecraft_folder, "versions/%s/%s.json" % (lastVersionId, lastVersionId))) and obj["lastVersionId"] == lastVersionId:
			profiles.pop(key, None)
		elif not options["moddedVersions"] and [] == version_list:
			profiles.pop(key, None)
		elif not options["notPlayedVersions"] and not played and obj["lastVersionId"] == lastVersionId:
			profiles.pop(key, None)
		elif not options["officialVersions"] and [] != version_list and obj["lastVersionId"] == lastVersionId:
			profiles.pop(key, None)
		elif not options["old_alpha"] and version_type == "old_alpha":
			profiles.pop(key, None)
		elif not options["old_beta"] and version_type == "old_beta":
			profiles.pop(key, None)
		elif not options["pendingVersions"] and version_type == "pending":
			profiles.pop(key, None)
		elif not options["playedVersions"] and played and obj["lastVersionId"] == lastVersionId:
			profiles.pop(key, None)
		elif not options["releases"] and version_type == "release" and obj["lastVersionId"] == lastVersionId:
			profiles.pop(key, None)
		elif not options["snapshots"] and version_type == "snapshot" and obj["lastVersionId"] == lastVersionId:
			profiles.pop(key, None)
		else:
			if options["hidePlayerSafetyDisclaimer"]:
				hidePlayerSafetyDisclaimer["%s_%s" % (lastVersionId, key)] = True

			if options["customGameDirForVersions"]:
				if options["customGameDir"] == "":
					obj["gameDir"] = os.path.join(minecraft_folder, "versions", lastVersionId)
				else:
					obj["gameDir"] = os.path.join(options["customGameDir"], "versions", lastVersionId)
			elif options["customGameDir"] != "":
				obj["gameDir"] = options["customGameDir"]
			
			if options["javaArgs"] != "":
				obj["javaArgs"] = options["javaArgs"]
				
			if options["sortBy"] == "releaseTime":
				obj["lastUsed"] = time
			elif options["sortBy"] == "created":
				obj["lastUsed"] = obj["created"]

			if options["autoNames"]:
				name = period_name(lastVersionId, version_type)
				obj["name"] = name

			if options["resolutionHeight"] > 0 or options["resolutionWidth"] > 0:
				obj["resolution"] = {}					
				if options["resolutionHeight"] >= 220:
					obj["resolution"]["height"] = options["resolutionHeight"]
	
				if options["resolutionWidth"] >= 280:
					obj["resolution"]["width"] = options["resolutionWidth"]

			print("	%s: %s" % (name, lastVersionId))

	launcher_profiles["profiles"] = dict(sorted(profiles.items()))
	json.dump(launcher_profiles, open(os.path.join(minecraft_folder, "launcher_profiles.json"), "w"), indent = 2)
	print("\33[32mFinished processing %s profiles\33[0m\nStarting configuring UISettings" % len(profiles))

	launcher_ui_state = {
		"data": {
			"UiEvents": "{}",
			"UiSettings": "{}"
		},
		"formatVersion" : 1
	}
	try:
		lines = b""
		comment = False
		for line in open(os.path.join(minecraft_folder, "launcher_ui_state.json"), "rb").readlines():
			if line.startswith(b"#$"):
				comment = True
			if not comment:
				lines += line
			if line.startswith(b"$#"):
				comment = False

		update_json(launcher_ui_state, json.loads(lines))
	except Exception as e:
		error_message('%s in launcher_ui_state.json: %s' % (type(e).__name__, e))

	data = launcher_ui_state["data"]
	if options["hidePlayerSafetyDisclaimer"]:
		UiEvents = {}
		try:
			UiEvents = json.loads(data["UiEvents"])
		except Exception as e:
			error_message('%s in launcher_ui_state.json: UiSettings: %s' % (type(e).__name__, e))
		UiEvents["hidePlayerSafetyDisclaimer"] = hidePlayerSafetyDisclaimer
		data["UiEvents"] = json.dumps(UiEvents, separators = (",", ":"))

	UiSettings = {
		"javaConfigurationFilter": {}
	}
	try:
		update_json(UiSettings, json.loads(data["UiSettings"]))
	except Exception as e:
		error_message('%s in launcher_ui_state.json: UiSettings: %s' % (type(e).__name__, e))

	javaConfigurationFilter = UiSettings["javaConfigurationFilter"]
	if options["sortBy"] == "name":
		javaConfigurationFilter["sortBy"] = "name"
	else:
		javaConfigurationFilter["sortBy"] = "last-played"

	UiSettings["javaConfigurationFilter"] = javaConfigurationFilter
	data["UiSettings"] = json.dumps(UiSettings, separators = (",", ":"))
	open(os.path.join(minecraft_folder, "launcher_ui_state.json"), "w").write("#$\nThis file is automatically generated by the Minecraft Launcher and is intended for internal use only.\nDO NOT EDIT\n$#\n" + json.dumps(launcher_ui_state, indent = 2))
	print("\33[32mFinished configuring settings.\33[0m")
except BaseException as e:
	error_message('%s: %s' % (type(e).__name__, e))

fail.close()