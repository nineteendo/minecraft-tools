import os
def Include(dir):
    for file in sorted(os.listdir(dir),reverse=True):
        path = dir+"/"+file
        if os.path.isdir(path):
            Include(path)
        else:
            file = file.replace('.json','')
            if not (file in includedItems or "template" in file or "elytra" in file or "trident" in file or "generated" in file or "handheld" in file or "bucket" in file or "dragon_breath" in file or "handheld" in file):
                    includedItems.append(file)
            for line in open(path,'r').readlines():
                if '"model":' in line:
                    item = line.split('/')[-1].split('"')[0]
                    if item in includedItems:
                        includedItems.remove(item)
def Exclude(dir):
    for file in os.listdir(dir):
        path = dir+"/"+file
        if os.path.isdir(path):
            Exclude(path)
        elif file != ".DS_Store":
            Type = ""
            for line in open(path,'r').readlines():
                if '"type":' in line and not 'uniform' in line and not "dynamic" in line:
                    Type=line[:-1].replace(',','').replace(' ','').replace('"','').replace('type:minecraft:','')
                if '"name":' in line and Type == "tag":
                    for line in open(directory+"/data/minecraft/tags/items/"+line[:-1].replace(',','').replace(' ','').replace('"','').split(':')[-1]+".json",'r').readlines():
                        if 'minecraft:' in line:
                            item = line[:-1].replace(',','').replace(' ','').replace('"','').split(':')[-1]
                            if item in includedItems:
                                includedItems.remove(item) 
                if '"name":' in line and Type in ["item",
                                                  "gift",
                                                  "barter",
                                                  "fishing"] or '"item":' in line and Type in ["crafting_shaped",
                                                                                               "smelting",
                                                                                               "stonecutting",
                                                                                               "crafting_shapeless",
                                                                                               "crafting_special_bookcloning",
                                                                                               "smoking",
                                                                                               "blasting",
                                                                                               "crafting_special_firework_star_fade",
                                                                                               "campfire_cooking",
                                                                                               "smithing",
                                                                                               "crafting_special_firework_rocket",
                                                                                               "crafting_special_shulkerboxcoloring",
                                                                                               "crafting_special_mapcloning",
                                                                                               "crafting_special_repairitem",
                                                                                               "crafting_special_bannerduplicate",
                                                                                               "crafting_special_armordye",
                                                                                               "crafting_special_tippedarrow",
                                                                                               "crafting_special_firework_star",
                                                                                               "crafting_special_mapextending",
                                                                                               "crafting_special_shielddecoration",
                                                                                               "crafting_special_suspiciousstew"]:
                    item = line[:-1].replace(',','').replace(' ','').replace('"','').split(':')[-1]
                    if item in includedItems and not item in ["potion","splash_potion","tipped_arrow","player_head","deepslate_copper_ore","deepslate_emerald_ore","deepslate_coal_ore"]:
                        includedItems.remove(item)
while True:
    try:
        includedItems = []
        directory = input("Default Data of Minecraft=")
        Include(directory+"/assets/minecraft/models/item/")
        Exclude(directory+"/data/minecraft/loot_tables/")
        Exclude(directory+"/data/minecraft/recipes/")
        for includedItem in sorted(includedItems):
            print(includedItem)
        break
    except:
        print(f"ERROR: No such file or directory: {directory}\n")
