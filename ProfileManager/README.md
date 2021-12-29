# OptionsManager
- fail.txt: file with the latest errors
- launcher_profiles.json: profiles for all notable versions
- options.json: settings (see below)
- profileManager.py: edit all your Minecraft profiles at once
- versions.csv: a table of the amount of versions from every category
- README.md: this file

# options.json
key | purpose
--- | ---
allVersions | create a profile for every version available (removes current ones)
autoNames | rename all profiles based upon predefined rules
customGameDir | set game directory for every profile
customGameDirForVersions | create a sub game directory under versions in the game directory for every single version
DEBUG_MODE | Show full error traceback
downloadVersions | download json for versions without one (otherwise removes profiles of them)
hidePlayerSafetyDisclaimer | hide safety pop-ups for all profiles
javaArgs | set java Virtual Machine Arguments for every profile
minecraftFolder | directory from the Minecraft launcher
moddedVersions | keep profiles for modded versions
notPlayedVersions | keep profiles for versions without jar
officialVersions | keep profiles for official versions
old_alpha | keep profiles for old_alpha versions
old_beta | keep profiles for old_beta versions
pendingVersions | keep profiles for pending versions
playedVersions | keep profiles for versions with jar
releases | keep profiles for releases
resolutionHeight | height in pixels of Minecraft
resolutionWidth | width in pixels of Minecraft
snapshots | keep profiles for snapshots
sortBy | sort profiles by *created*, *name*, *last-played* or *releaseTime*
specialVersions | versions you want to give a custom name
stringReplace | strings in a version to replace in order
typeNames | version types with a custom prefix