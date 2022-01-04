import os, sys, json, platform, traceback

options = {
	"backupOptions": True,
	"DEBUG_MODE": False,
	"minecraftFolder": {
		"Darwin": "~/Library/Application Support/minecraft",
		"Linux": "~/.minecraft",
		"Windows": "%APPDATA%/.minecraft"
	},
	"renameOptions": True,
	"showChanges": False
}

renamed_options = {
	"clouds": "renderClouds",
	"key_Back": "key_key.back",
	"key_Build": "key_key.use",
	"key_Chat": "key_key.chat",
	"key_Drop": "key_key.drop",
	"key_Forward": "key_key.forward",
	"key_Inventory": "key_key.inventory",
	"key_Jump": "key_key.jump",
	"key_Left": "key_key.left",
	"key_Right": "key_key.right",
	"key_Sneak": "key_key.sneak",
	"key_key.back": "key_Back",
	"key_key.chat": "key_Chat",
	"key_key.drop": "key_Drop",
	"key_key.forward": "key_Forward",
	"key_key.inventory": "key_Inventory",
	"key_key.jump": "key_Jump",
	"key_key.left": "key_Left",
	"key_key.right": "key_Right",
	"key_key.sneak": "key_Sneak",
	"key_key.swapHands": "key_key.swapOffhand",
	"key_key.swapOffhand": "key_key.swapHands",
	"key_key.use": "key_Build",
	"modelPart_cape": "showCape",
	"renderClouds": "clouds",
	"showCape": "modelPart_cape",
	"soundCategory_animals": "soundCategory_neutral",
	"soundCategory_block": "soundCategory_blocks",
	"soundCategory_blocks": "soundCategory_block",
	"soundCategory_hostile": "soundCategory_mobs",
	"soundCategory_mobs": "soundCategory_hostile",
	"soundCategory_neutral": "soundCategory_animals",
	"soundCategory_player": "soundCategory_players",
	"soundCategory_players": "soundCategory_player",
	"soundCategory_record": "soundCategory_records",
	"soundCategory_records": "soundCategory_record"
}

mappings = {
	"key.mouse.left": "-100",
	"key.mouse.right": "-99",
	"key.mouse.middle": "-98",
	"key.keyboard.unknown": "0",
	"key.keyboard.escape": "1",
	"key.keyboard.1": "2",
	"key.keyboard.2": "3",
	"key.keyboard.3": "4",
	"key.keyboard.4": "5",
	"key.keyboard.5": "6",
	"key.keyboard.6": "7",
	"key.keyboard.7": "8",
	"key.keyboard.8": "9",
	"key.keyboard.9": "10",
	"key.keyboard.0": "11",
	"key.keyboard.minus": "12",
	"key.keyboard.equal": "13",
	"key.keyboard.backspace": "14",
	"key.keyboard.tab": "15",
	"key.keyboard.q": "16",
	"key.keyboard.w": "17",
	"key.keyboard.e": "18",
	"key.keyboard.r": "19",
	"key.keyboard.t": "20",
	"key.keyboard.y": "21",
	"key.keyboard.u": "22",
	"key.keyboard.i": "23",
	"key.keyboard.o": "24",
	"key.keyboard.p": "25",
	"key.keyboard.left.bracket": "26",
	"key.keyboard.right.bracket": "27",
	"key.keyboard.enter": "28",
	"key.keyboard.left.control": "29",
	"key.keyboard.a": "30",
	"key.keyboard.s": "31",
	"key.keyboard.d": "32",
	"key.keyboard.f": "33",
	"key.keyboard.g": "34",
	"key.keyboard.h": "35",
	"key.keyboard.j": "36",
	"key.keyboard.k": "37",
	"key.keyboard.l": "38",
	"key.keyboard.semicolon": "39",
	"key.keyboard.apostrophe": "40",
	"key.keyboard.grave.accent": "41",
	"key.keyboard.left.shift": "42",
	"key.keyboard.backslash": "43",
	"key.keyboard.z": "44",
	"key.keyboard.x": "45",
	"key.keyboard.c": "46",
	"key.keyboard.v": "47",
	"key.keyboard.b": "48",
	"key.keyboard.n": "49",
	"key.keyboard.m": "50",
	"key.keyboard.comma": "51",
	"key.keyboard.period": "52",
	"key.keyboard.slash": "53",
	"key.keyboard.right.shift": "54",
	"key.keyboard.keypad.multiply": "55",
	"key.keyboard.left.alt": "56",
	"key.keyboard.space": "57",
	"key.keyboard.caps.lock": "58",
	"key.keyboard.f1": "59",
	"key.keyboard.f2": "60",
	"key.keyboard.f3": "61",
	"key.keyboard.f4": "62",
	"key.keyboard.f5": "63",
	"key.keyboard.f6": "64",
	"key.keyboard.f7": "65",
	"key.keyboard.f8": "66",
	"key.keyboard.f9": "67",
	"key.keyboard.f10": "68",
	"key.keyboard.num.lock": "69",
	"key.keyboard.scroll.lock": "70",
	"key.keyboard.keypad.7": "71",
	"key.keyboard.keypad.8": "72",
	"key.keyboard.keypad.9": "73",
	"key.keyboard.keypad.subtract": "74",
	"key.keyboard.keypad.4": "75",
	"key.keyboard.keypad.5": "76",
	"key.keyboard.keypad.6": "77",
	"key.keyboard.keypad.add": "78",
	"key.keyboard.keypad.1": "79",
	"key.keyboard.keypad.2": "80",
	"key.keyboard.keypad.3": "81",
	"key.keyboard.keypad.0": "82",
	"key.keyboard.keypad.decimal": "83",
	"key.keyboard.f11": "87",
	"key.keyboard.f12": "88",
	"key.keyboard.f13": "100",
	"key.keyboard.f14": "101",
	"key.keyboard.f15": "102",
	"key.keyboard.f16": "103",
	"key.keyboard.f17": "104",
	"key.keyboard.f18": "105",
	"key.keyboard.f19": "113",
	"key.keyboard.keypad.equal": "141",
	"key.keyboard.keypad.enter": "156",
	"key.keyboard.right.control": "157",
	"key.keyboard.right": "171",
	"key.keyboard.end": "173",
	"key.keyboard.down": "174",
	"key.keyboard.page.down": "175",
	"key.keyboard.insert": "176",
	"key.keyboard.delete": "177",
	"key.keyboard.left.win": "185",
	"key.keyboard.right.win": "186",
	"key.keyboard.right": "205",
	"key.keyboard.end": "207",
	"key.keyboard.down": "208",
	"key.keyboard.page.down": "209",
	"key.keyboard.insert": "210",
	"key.keyboard.delete": "211",
	"key.keyboard.left.win": "219",
	"key.keyboard.right.win": "220"
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

def rename_value(dictionary, key, value):
	if key in renamed_options and options["renameOptions"]:
		downgrade_value(dictionary, renamed_options[key], value)
	
	downgrade_value(dictionary, key, value)

def downgrade_value(dictionary, key, value):
	# Fix key mappings for old versions
	if value in mappings:
		value = mappings[value]
	elif value.startswith("key.mouse."):
		try:
			value = int(value.removeprefix("key.mouse.")) - 101
		except Exception:
			pass
			
	# Fix language format for old versions
	if key == "lang" and "_" in value:
		tupel = value.split("_")
		value = tupel[0] + "_" + tupel[-1].upper()
	
	# Force option Upgrade
	if key == "version":
		value = "0"
	
	# Fix changed format for sound and music
	if key in ["sound", "music"] and value == "1.0":
		value = "true"
			
	dictionary[key] = value

try:
	fail = open("fail.txt", "w")
	print("\033[95m\033[1mMinecraft Options Manager v1.1.0\n(C) 2021 by Nineteendo\033[0m")
	try:
		update_json(options, json.load(open(os.path.join(sys.path[0], "options.json"), "rb")))
	except Exception as e:
		error_message("%s in options.json: %s" % (type(e).__name__, e))
		
	if platform.system() in options["minecraftFolder"]:
		path = os.path.expanduser(options["minecraftFolder"][platform.system()])
	else:
		raise SystemError("Unknown system: %s" % platform.system())
	
	all_options = {}
	if options["backupOptions"]:
		try:
			for line in open(os.path.join(path, "options_old.txt"),"r").readlines():
				key, value = line.split(":")
				rename_value(all_options, key, value.strip("\n"))
		except Exception:
			pass
	
	new_options = {}
	try:
		for line in open(os.path.join(path, "options.txt"),"r").readlines():
			key, value = line.split(":")
			rename_value(new_options, key, value.strip("\n"))
	except Exception:
		new_options = all_options
		error_message(os.path.join(path, "options.txt") + " is missing.")
	
	if options["backupOptions"] and options["showChanges"]:
		for option in sorted(all_options):
			value = all_options[option]
			if not option in new_options:
				print("\33[91m-MISSING\t%s\t%s\033[0m" % (option, value))
	
		for option in sorted(new_options):
			value = new_options[option]
			if not option in all_options:
				print("\33[32m+ADDED\t%s\t%s\033[0m" % (option, value))
		
			all_options[option] = value
	else:
		all_options = new_options
	
	if all_options == {}:
		print("\33[91mFailed to load options.\033[0m")
	else:
		options_new = open(os.path.join(path, "options.txt"),"w")
		for key in sorted(all_options):
			options_new.write("%s:%s\n" % (key, all_options[key]))
		
		options_new.close()
		if options["backupOptions"]:
			open(os.path.join(path, "options_old.txt"),"w").write(open(os.path.join(path, "options.txt"),"r").read())
			print("\n\33[32mFixed options and made backup.\033[0m")
		else:
			print("\n\33[32mFixed options\033[0m")
except BaseException as e:
	error_message("%s: %s" % (type(e).__name__, e))

fail.close()
