import os, shutil
def chmod(path):
	if os.path.exists(path):
		  os.chmod(path, 0o777)     
	if os.path.isdir(path):
		for file in sorted(os.listdir(path)):
			chmod(os.path.join(path, file))
shutil.move("/Applications/Minecraft.app/Contents", "/Applications/Minecraft.app/Contents2")
shutil.move("/Applications/Minecraft.app/Contents2", "/Applications/Minecraft.app/Contents")
chmod("/Applications/Minecraft.app/Contents")