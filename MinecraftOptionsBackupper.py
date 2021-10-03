import os, platform

print("\n\033[95m\033[1mMinecraft Options Backupper v1.0.0\n(C) 2021 by Nineteendo\033[0m\n")
if (platform.system() == "Darwin"):
	path = os.path.expanduser('~/Library/Application Support/minecraft/')
elif (platform.system() == "Linux"):
	path = os.path.expanduser('~/.minecraft/')
elif (platform.system() == "Windows"):
	path = os.path.expandvars('%APPDATA%\.minecraft/')
else:
	print("Unknown system: %s" % platform.system())
all_options = {}
try:
    options = open(path + "options.txt",'r')
    for line in options.readlines():
        option = line.split(':')[0]
        value = line.split(':')[-1]
        if not option in all_options:
            if option == "lang" and "_" in value:
                value = value.split('_')[0] + "_" + value.split('_')[-1].upper()
            all_options[option] = value
    options.close()
except:
    print(path + "options.txt is missing. Attempting to load backup...")   
try:
	options_old = open(path + "options_old.txt",'r')
	for line in options_old.readlines():
		option = line.split(':')[0]
		value = line.split(':')[-1]
		if not option in all_options:
			all_options[option] = value
	options_old.close()
except:
	print("Thanks for using this tool for the first time.")
if all_options != {}:
    options = open(path + "options.txt",'w')
    for key in all_options:
            options.write(key+":"+all_options[key])
    options.close()
    options_old = open(path + "options_old.txt",'w')
    for key in all_options:
            options_old.write(key+":"+all_options[key])
    options_old.close()
    print("Succesfuly merged options and made backup.")
else:
	print("Failed to load backup.")
input("\nFinished. Press Enter\n")
