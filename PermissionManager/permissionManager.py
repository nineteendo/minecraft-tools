import os, shutil

def chmod(path):
	if os.path.exists(path):
		  os.chmod(path, 0o777)     
	if os.path.isdir(path):
		for file in sorted(os.listdir(path)):
			chmod(os.path.join(path, file))

try:
	print("\n\033[95m\033[1mMinecraft Permission Manager v1.1.0\n(C) 2021 by Nineteendo\033[0m\n")
	chmod("/Applications/Minecraft.app/Contents")
except BaseException as e:
	print('\n\33[91m%s: %s\33[0m' % (type(e).__name__, e))
