import os
for file in os.listdir():
    if os.path.isfile(file) and os.path.splitext(file)[-1] == ".json":
        keys=""
        criteria=""
        result=""
        for line in open(file,'r').readlines():
            if 'item' in line and result == "":
                key=line.split(':')[-1].strip('"\n')
                keys+='''    "has_%s": {
      "trigger": "minecraft:inventory_changed",
      "conditions": {
        "items": [
          {
            "item": "minecraft:%s"
          }
        ]
      }
    },\n''' % (key,key)
                criteria+='      "has_%s",\n' % key
            if 'item' in line and result != "" or 'result' in line:
                result = line.split(':')[-1].strip('",\n')   
        if (keys!=""):
             open(file,'w').write('''{
   "parent": "minecraft:recipes/root",
   "rewards": {
     "recipes": [
       "minecraft:%s"
     ]
   },
   "criteria": {
%s     "has_the_recipe": {
       "trigger": "minecraft:recipe_unlocked",
       "conditions": {
         "recipe": "minecraft:%s"
       }
     }
   },
   "requirements": [
     [
%s       "has_the_recipe"
     ]
   ]
 }''' %(os.path.splitext(file)[0],keys,result,criteria))
