# JSON NBTencoder
# written by Nineteendo

import os, json, struct, gzip

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

# Dictionary for Data Types in human language
mappings = {
	b"\x01": ["number","numbers"],
	b"\x02": ["number","numbers"],
	b"\x03": ["number","numbers"],
	b"\x04": ["number","numbers"],
	b"\x05": ["number","numbers"],
	b"\x06": ["number","numbers"],
	b"\x07": ["list of numbers","list of numbers"],
	b"\x08": ["text","texts"],
	b"\x09": ["list","lists"],
	b"\x0a": ["dictionary","dictionaries"],
	b"\x0b": ["list of numbers","list of numbers"],
	b"\x0c": ["list of numbers","list of numbers"]
}

# Options
options = {
	"AllowNan": True,
	"AutoBool": True,
	"AutoInt": False,
	"DefaultJSONPath": "jsons/",
	"EnsureAscii": False,
	"Indent": "\t",
	"DefaultNBTPath": "nbts/",
	"BigEndian": None,
	"RepairFiles": False,
	"CommaSeparator": " ",
	"DoublePointSeparator": " ",
	"SortKeys": False,
	"UncompressedFiles": (
		".mcstructure",
		".nbt",
		"/servers.dat",
		"/servers.dat_old"
	)
}

def encode_string(string, byteorder):
	return struct.pack(byteorder + "H", len(string.encode('utf-8'))) + string.encode('utf-8')
	
def encode_number(integ, byteorder, isint = True, override = end):
	if isint and -128 <= integ <= 127 and not override in [int16, float32, int32, float64, int64]:
		return (int8, struct.pack(byteorder + 'b', integ))
	elif isint and -32768 <= integ <= 32767 and not override in [float32, int32, float64, int64]:
		return (int16, struct.pack(byteorder + 'h', integ))
	elif isint and -2147483648 <= integ <= 2147483647 and not override in [float32, float64, int64]:
		return (int32, struct.pack(byteorder + 'i', integ))
	elif isint and -9223372036854775808 <= integ <= 9223372036854775807 and not override in [float32, float64]:
		return (int64, struct.pack(byteorder + 'q', integ))
	elif -340282346638528859811704183484516925440 <= integ <= 340282346638528859811704183484516925440 and integ == struct.unpack('>f', struct.pack('>f', integ))[0] and override != float64:
		if isint and not options["AutoInt"]:
			print("\33[33mWARNING: storing %s as decimal number\33[0m" % integ)
		return (float32, struct.pack(byteorder + "f", integ))
	else:
		if isint and not options["AutoInt"]:
			print("\33[33mWARNING: storing %s as decimal number\33[0m" % integ)
		return (float64, struct.pack(byteorder + "d", integ))

def encode_list(data, byteorder, override = end):
	tag = end
	special = end
	string = struct.pack(byteorder + 'I', len(data))
	for k, v in enumerate(data):
		tupel = encode_json(v, byteorder)
		newtag = tupel[0]
		if isinstance(v, int) or isinstance(v, float) and v.is_integer():
			if v != struct.unpack('>d', struct.pack(">d", v))[0]:
				special = int64
			elif special != int64 and -340282346638528859811704183484516925440 <= v <= 340282346638528859811704183484516925440 and v != struct.unpack('>f', struct.pack(">f", v))[0]:
				special = int32
		
		if isinstance(v, bool) and special != list32 and tag in [end, int8, int16, float32, int32, float64, int64]: # Boolian
			if special == end:
				special = string16
		elif v == [] and special in [end, list32] and tag in [end, list32, int8_list32, int32_list32, int64_list32]: # Empty list
			special = list32
		elif tag != newtag:
			if tag == end and (special in [end, int32, int64] or (special == list32 and newtag in [list32, int8_list32, int32_list32, int64_list32]) or (special in string16 and newtag in [int8, int16, float32, int32, float64, int64, string16])):
				tag = newtag
			elif tag in [list32, int8_list32, int32_list32, int64_list32] and newtag in [list32, int8_list32, int32_list32, int64_list32]:
				tag = list32
			elif tag in [int8, int16, float32, int32, float64, int64] and newtag in [int8, int16, float32, int32, float64, int64]:
				if special == int64 and (tag in [float32, float64] or newtag in [float32, float64]):
					raise TypeError("Found big %s in a list of big %s: %s" % (mappings[newtag][0], mappings[tag][1], v))
				elif special == int32 and (tag in [float32, float64] or newtag in [float32, float64]):
					tag = float64
				elif newtag == int64 or (tag != int64  and (newtag == int32 or (tag != int32  and (newtag == float32 or (tag != float32 and newtag == int16))))):
					tag = newtag
			else:
				raise TypeError("Found %s in a list of %s: %s" % (mappings[newtag][0], mappings[tag][1], v))
				
	if tag == end and special != end:
		tag = special
		
	for v in data:
		tupel = encode_json(v, byteorder, tag)
		string += tupel[1]
		
	if override == list32:
		return (list32, tag + string)
	elif tag == int8 or override == int8_list32:
		return (int8_list32, string)
	elif tag == int32 or override == int32_list32:
		return (int32_list32, string)
	elif tag == int64 or override == int64_list32:
		return (int64_list32, string)
	else:
		return (list32, tag + string)

def encode_object16(data, byteorder, override = end):
	string = b""
	for v in data[:-1]:
		value = encode_json(v, byteorder)
		string += value
	return string
	
def encode_json(data, byteorder, override = end):
	if isinstance(data, list):
		if len(data) == 0 or not isinstance(data[0], tuple):
			return encode_list(data, byteorder, override)
		else:
			return (object16, encode_object16(data, byteorder, override) + end)	
	elif isinstance(data, tuple):
		key = encode_string(data[0], byteorder)
		tupel = encode_json(data[1], byteorder)
		tag = tupel[0]
		value = tupel[1]
		return tag + key + value
	elif isinstance(data, bool) and override in [end, string16]:
		return (string16, encode_string(str(data).lower(), byteorder))
	elif isinstance(data, int):
		return encode_number(data, byteorder, True, override)
	elif isinstance(data, float):
		if data.is_integer() and options["AutoInt"]:
			return encode_number(int(data), byteorder, True, override)
		else:
  			return encode_number(data, byteorder, False, override)
	elif isinstance(data, str):
		return (string16, encode_string(data, byteorder))
	else:
		raise TypeError(type(data).__name__)

def conversion(inp,out):
	if os.path.isdir(inp):
		os.makedirs(out, exist_ok=True)
		for entry in sorted(os.listdir(inp)):
			conversion(os.path.join(inp, entry),os.path.join(out, entry))
	elif os.path.isfile(inp) and inp.endswith('.json'):
		write = out.removesuffix(".json")
		try:
			data=json.load(open(inp, 'rb'), object_pairs_hook=encode_object_pairs)
		except:
			print("\33[91mno json: %s\33[0m" % inp)
		else:
			try:
				if options["BigEndian"] or options["BigEndian"] == None and not write.endswith("_BE"):
					byteorder = ">"
				else:
					byteorder = "<"
					
				write = write.removesuffix("_BE")
				output = encode_object16(data, byteorder)
				if write.endswith(options["UncompressedFiles"]):
					open(write, 'wb').write(output)
				else:
					gzip.open(write, 'wb').write(output)
					
				print("wrote " + write)
			except Exception as e:
				print('\33[91m%s in %s: %s\33[0m' % (type(e).__name__, inp, e))

def encode_object_pairs(pairs):
	if options["SortKeys"]:
		pairs = sorted(pairs)
		
	pairs.append(("",""))
	return pairs

print("\033[95m\033[1mJSONS NBTencoder v1.0.0\n(C) 2021 by Nineteendo\033[0m\n")
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
	inp = input("\033[1mInput file or directory:\033[0m ")
	if os.path.isfile(inp):
		out = input("\033[1mOutput file:\033[0m ") + ".json"
	else:
		out = input("\033[1mOutput directory:\033[0m ")
except Exception:
	inp = options["DefaultJSONPath"]
	out = options["DefaultNBTPath"]
	os.makedirs(inp, exist_ok=True)

print(inp,">",out)

# Start conversion
conversion(inp,out)