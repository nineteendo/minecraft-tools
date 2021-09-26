import os, json, struct, gzip

End = b"\x00"
Int8 = b"\x01"
Int16 = b"\x02"
Int32 = b"\x03"
Int64 = b"\x04"
Float = b"\x05"
Double = b"\x06"
Int8_List = b"\x07"
String = b"\x08"
List = b"\x09"
Object = b"\x0a"
Int32_List = b"\x0b"
Int64_List = b"\x0c"

def parse_int8(fp):
	return struct.unpack('b', fp.read(1))[0]
	
def parse_int16(fp):
	return struct.unpack('>h', fp.read(2))[0]
	
def parse_int32(fp):
	return struct.unpack('>i', fp.read(4))[0]
	
def parse_int64(fp):
	return struct.unpack('>q', fp.read(8))[0]
	
def parse_float(fp):
	return struct.unpack('>f', fp.read(4))[0]
	
def parse_double(fp):
	return struct.unpack('>d', fp.read(8))[0]
	
def parse_int8_array(fp):
	return parse_array(fp, Int8)
	
def parse_string(fp):
	return fp.read(struct.unpack('>H', fp.read(2))[0]).decode('utf-8')
	
def parse_list(fp):
	return parse_array(fp, fp.read(1))
	
def parse_int32_array(fp):
	return parse_array(fp, Int32)
	
def parse_int64_array(fp):
	return parse_array(fp, Int64)

def parse_array(fp, code):
	result = []
	lenght = parse_int32(fp)
	if code == End:
		return result
	if code in mappings:
		for i in range(lenght):
			result.append(mappings[code](fp))
	return result
	
def parse_compound(fp):
	result = {}

	try:
		while True:
			tuple = parse(fp)
			result[tuple[0]] = tuple[-1]
	except KeyError as k:
		if k.args[0] == b'':
			print("\n	SilentError: %s pos %s: End of file" %(fp.name,fp.tell()-1))
		else:
			raise k
	except StopIteration:
		pass
	
	return result

def parse(fp):
	code = fp.read(1)
	if code == End:
		raise StopIteration
	return (parse_string(fp), mappings[code](fp))

def conversion(inp,out):
	if os.path.isdir(inp):
		os.makedirs(out, exist_ok=True)
		for entry in sorted(os.listdir(inp)):
			conversion(os.path.join(inp, entry),os.path.join(out, entry))
	elif os.path.isfile(inp) and not inp.endswith('.' + 'json'):
		split = os.path.splitext(out)
		jfn=split[0]+split[1].replace(".dat","").replace(".nbt","")+'.json'
		try:
			# Header check
			if open(inp,"rb").read(2) == b"\x1F\x8B":
				file = gzip.open(inp,"rb")
			else:
				file = open(inp,"rb")
			data = parse(file)[-1]
			open(jfn, 'wb').write(json.dumps(data, ensure_ascii=False,indent=4).encode('utf8'))
			print('wrote '+format(jfn))
		except Exception as e:
			print('\n%s in %s pos %s: %s' % (type(e).__name__, inp, file.tell()-1, e))

mappings = {
	b"\x01": parse_int8,
	b"\x02": parse_int16,
	b"\x03": parse_int32,
	b"\x04": parse_int64,
	b"\x05": parse_float,
	b"\x06": parse_double,
	b"\x07": parse_int8_array,
	b"\x08": parse_string,
	b"\x09": parse_list,
	b"\x0a": parse_compound,
	b"\x0b": parse_int32_array,
	b"\x0c": parse_int64_array
	}

#fail=open("fail.txt","w")
#fail.write("fails:")
print("NBTParser v1.0.0\nby Nineteendo")
try:
	inp = input("Input file or directory:")
	out = os.path.join(input("Output directory:"),os.path.basename(inp))
except:
	inp = "nbts/"
	out = "jsons/"
	os.makedirs(inp, exist_ok=True)

print(inp,">",out)
conversion(inp,out)
#fail.close()
#try:
#	os.startfile("fail.txt")
#except:
#	try:
#		os.system("open fail.txt")
#	except:
#		os.system("xdg-open fail.txt")