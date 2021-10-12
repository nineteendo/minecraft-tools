# NBT parser (ALPHA!)
# written by Nineteendo
# usage: put nbt files in nbts & run
import os, json, struct, gzip

end = b"\x00"
int8 = b"\x01"
int16 = b"\x02"
int32 = b"\x03"
int64 = b"\x04"
float32 = b"\x05"
float64 = b"\x06"
int8_list32 = b"\x07"
string16 = b"\x08"
list32 = b"\x09"
object16 = b"\x0a"
int32_list32 = b"\x0b"
int64_list32 = b"\x0c"

def parse_int8(fp):
	return struct.unpack('b', fp.read(1))[0]
	
def parse_int16(fp):
	return struct.unpack('>h', fp.read(2))[0]
	
def parse_int32(fp):
	return struct.unpack('>i', fp.read(4))[0]
	
def parse_int64(fp):
	return struct.unpack('>q', fp.read(8))[0]
	
def parse_float32(fp):
	return struct.unpack('>f', fp.read(4))[0]
	
def parse_float64(fp):
	return struct.unpack('>d', fp.read(8))[0]
	
def parse_int8_list32(fp):
	return parse_list32_code(fp, int8)
	
def parse_string(fp):
	string = fp.read(struct.unpack('>H', fp.read(2))[0]).decode('utf-8')
	if string.lower() in ["false","true"]:
		return string.lower == "true"
	else:
		return string
	
def parse_list(fp):
	return parse_list32_code(fp, fp.read(1))
	
def parse_int32_list32(fp):
	return parse_list32_code(fp, int32)
	
def parse_int64_list32(fp):
	return parse_list32_code(fp, int64)

def parse_list32_code(fp, code):
	result = []
	lenght = parse_int32(fp)
	if code == end:
		return result
	if code in mappings:
		for i in range(lenght):
			result.append(mappings[code](fp))
	return result
	
class FakeDict(dict):
	def __init__(self, items):
		self['something'] = 'something'
		self._items = items
	def items(self):
		return self._items

def parse_object16(fp):
	result = []

	try:
		while True:
			tuple = parse(fp)
			result.append((tuple[0],tuple[-1]))
	except KeyError as k:
		if k.args[0] == b'':
			print("\n	SilentError: %s pos %s: end of file" %(fp.name,fp.tell()-1))
		else:
			raise k
	except StopIteration:
		pass
	
	return FakeDict(result)

def parse(fp):
	code = fp.read(1)
	if code == end:
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
	b"\x05": parse_float32,
	b"\x06": parse_float64,
	b"\x07": parse_int8_list32,
	b"\x08": parse_string,
	b"\x09": parse_list,
	b"\x0a": parse_object16,
	b"\x0b": parse_int32_list32,
	b"\x0c": parse_int64_list32
	}

#fail=open("fail.txt","w")
#fail.write("fails:")
print("\033[95m\033[1mNBTParser v1.0.0\n(C) 2021 by Nineteendo\033[0m\n")
try:
	inp = input("\033[1mInput file or directory:\033[0m ")
	out = input("\033[1mOutput directory:\033[0m ")
	if os.path.isfile(inp):
		out = os.path.join(out,os.path.basename(inp))
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