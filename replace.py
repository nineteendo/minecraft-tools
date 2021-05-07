import os
while True:
    find = bytes(input('Find=').replace(r'\n', '\n'), 'utf-8')
    replace = bytes(input('Replace=').replace(r'\n', '\n'), 'utf-8')
    for file in os.listdir():
        if os.path.isfile(file) and os.path.splitext(file)[-1] == ".json":
            f=open(file,'rb')
            s=f.read()
            f.close()
            s=s.replace(find,replace)
            open(file,'wb').write(s)
