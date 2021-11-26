# NBT parser
# written by Nineteendo
# usage: put nbt files in nbts & run
import os, json, struct, gzip, zipfile

# Data Types
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

# Default Options
options = {
	"AllowNan": True,
	"AutoBool": True,
	"AutoInt": False,
	"BigEndian": None,
	"CommaSeparator": "",
	"DoublePointSeparator": " ",
	"EnsureAscii": False,
	"Indent": "\t",
	"NBTExtensions": (
		".dat",
		".dat_mcr",
		".dat_old",
		".mcstructure",
		".nbt"
	),
	"RepairFiles": False,
	"SortKeys": False,
	"UncompressedFiles": (
		"_BE",
		".mcstructure",
		".nbt",
		"/servers.dat",
		"/servers.dat_old"
	)
}

edition = {
	">": "Java Edition",
	"<": "Bedrock Edition"
} 

# More versatile dictionaries
class FakeDict(dict):
	def __init__(self, items):
		self._items = items
		if items != []:
			self['something'] = 'something'
	
	def items(self):
		return self._items

def parse_int8(fp, byteorder):
	return struct.unpack('b', fp.read(1))[0]
	
def parse_int16(fp, byteorder):
	return struct.unpack(byteorder + 'h', fp.read(2))[0]
	
def parse_int32(fp, byteorder):
	return struct.unpack(byteorder + 'i', fp.read(4))[0]
	
def parse_int64(fp, byteorder):
	return struct.unpack(byteorder + 'q', fp.read(8))[0]
	
def parse_float32(fp, byteorder):
	return struct.unpack(byteorder + 'f', fp.read(4))[0]
	
def parse_float64(fp, byteorder):
	return struct.unpack(byteorder + 'd', fp.read(8))[0]
	
def parse_string16(fp, byteorder):
	string = fp.read(struct.unpack(byteorder + 'H', fp.read(2))[0]).decode('utf-8')
	if options["AutoBool"] and string.lower() in ["false","true"]:
		return string.lower == "true"
	else:
		return string
	
def parse_list32(fp, byteorder):
	return parse_list32_code(fp, fp.read(1), byteorder)
	
def parse_int8_list32(fp, byteorder):
	return parse_list32_code(fp, int8, byteorder)

def parse_int32_list32(fp, byteorder):
	return parse_list32_code(fp, int32, byteorder)
	
def parse_int64_list32(fp, byteorder):
	return parse_list32_code(fp, int64, byteorder)

def parse_list32_code(fp, code, byteorder):
	result = []
	lenght = struct.unpack(byteorder + 'I', fp.read(4))[0]
	if code == end:
		return result
		
	if code in mappings:
		for i in range(lenght):
			result.append(mappings[code](fp, byteorder))
	return result

def parse_root_object16(fp, byteorder):
	result = []
	try:
		while True:
			tupel = parse(fp, byteorder)
			result.append(tupel)
			
	except KeyError as k:
		if k.args[0] == b'':
			return FakeDict(result)
		else:
			raise k

def parse_object16(fp, byteorder):
	result = []
	try:
		while True:
			tupel = parse(fp, byteorder)
			result.append(tupel)
	except KeyError as k:
		if str(k) == "b''":
			if options["RepairFiles"]:
				print("\33[33mWARNING failed %s parse: %s pos %s: end of file\33[0m" %(edition[byteorder], fp.name,fp.tell()-1))
			else:
				raise EOFError
		else:
			raise TypeError("unknown tag %s" %k)
	except struct.error: # struct.error: Unpack requires a buffer of XX bytes
		if options["RepairFiles"]:
			print("\33[33mWARNING failed %s parse: %s pos %s: end of file\33[0m" %(edition[byteorder], fp.name,fp.tell()-1))
		else:
			raise EOFError
	except StopIteration:
		pass
	
	return FakeDict(result)

def parse(fp, byteorder):
	code = fp.read(1)
	if code == end:
		raise StopIteration
		
	function = mappings[code]
	return (parse_string16(fp, byteorder), function(fp, byteorder))

# Parse Functions
mappings = {
	b"\x01": parse_int8,
	b"\x02": parse_int16,
	b"\x03": parse_int32,
	b"\x04": parse_int64,
	b"\x05": parse_float32,
	b"\x06": parse_float64,
	b"\x07": parse_int8_list32,
	b"\x08": parse_string16,
	b"\x09": parse_list32,
	b"\x0a": parse_object16,
	b"\x0b": parse_int32_list32,
	b"\x0c": parse_int64_list32
}

def conversion(inp,out):
	if os.path.isdir(inp) and os.path.realpath(inp) != os.path.realpath(pathout):
		os.makedirs(out, exist_ok=True)
		for entry in sorted(os.listdir(inp)):
			conversion(os.path.join(inp, entry),os.path.join(out, entry))
	elif os.path.isfile(inp) and inp.endswith(options["NBTExtensions"]):
		# Header check
		if open(inp,"rb").read(2) == b"\x1F\x8B":
				file = gzip.open(inp,"rb")
		else:
			file = open(inp,"rb")
			
		exception = ""
		try:
			jfn = out + '.json'
			data = parse_root_object16(file, ">")
			json.dump(data, open(jfn, 'w'), allow_nan = options["AllowNan"], ensure_ascii = options["EnsureAscii"], indent = options["Indent"], separators = ("," + options["CommaSeparator"], ":" + options["DoublePointSeparator"]), sort_keys = options["SortKeys"])
			print('wrote %s' % jfn)
		except Exception as e:
			exception = '\33[91mFailed %s parse: %s in %s pos %s: %s\33[0m' % (edition[">"], type(e).__name__, inp, file.tell()-1, e)
			
		if open(inp,"rb").read(2) == b"\x1F\x8B":
				file = gzip.open(inp,"rb")
		else:
			file = open(inp,"rb")
			
		try:
			jfn = out + "_BE" + '.json'
			data = parse_root_object16(file, "<")
			json.dump(data, open(jfn, 'w'), allow_nan = options["AllowNan"], ensure_ascii = options["EnsureAscii"], indent = options["Indent"], separators = ("," + options["CommaSeparator"], ":" + options["DoublePointSeparator"]), sort_keys = options["SortKeys"])
			print('wrote %s' % jfn)
		except Exception as e:
			if exception:
				print(exception)
				print('\33[91mFailed %s parse: %s in %s pos %s: %s\33[0m' % (edition["<"], type(e).__name__, inp, file.tell()-1, e))

print("\033[95m\033[1mNBTParser v1.0.0\n(C) 2021 by Nineteendo\033[0m\n")
print("Working directory: %s" % os. getcwd())	
try:
	newoptions = json.load(open("options.json", "rb"))
	for key in options:
		if key in newoptions and newoptions[key] != options[key]:
			if type(options[key]) == type(newoptions[key]):
				options[key] = newoptions[key]
			elif isinstance(options[key], tuple) and isinstance(newoptions[key], list):
				options[key] = tuple([str(i) for i in newoptions[key]])
			elif options[key] == None and isinstance(newoptions[key], bool):
				options[key] = newoptions[key]
			elif key == "Indent" and type(newoptions[key]) in [int, type(None)]:
				options[key] = newoptions[key]
except:
	print("\33[91mFailed to load options.json\33[0m")

try:
	pathin = input("\033[1mInput file or directory\033[0m: ")
	if os.path.isfile(pathin):
		pathout = input("\033[1mOutput file\033[0m: ").removesuffix(".json")
	else:
		pathout = input("\033[1mOutput directory\033[0m: ")
	
	# Start conversion
	conversion(pathin,pathout)
except BaseException as e:
	print('\n\33[91m%s: %s\33[0m' % (type(e).__name__, e))
