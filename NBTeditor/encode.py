# JSON parser (ALPHA!)
# written by Nineteendo
# usage: put json files in jsons & run

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

mappings = {
	b"\x01": ["number","numbers"],
	b"\x02": ["number","numbers"],
	b"\x03": ["number","numbers"],
	b"\x04": ["number","numbers"],
	b"\x05": ["decimal number","decimal numbers"],
	b"\x06": ["decimal number","decimal numbers"],
	b"\x07": ["list of numbers","list of numbers"],
	b"\x08": ["text","texts"],
	b"\x09": ["list","lists"],
	b"\x0a": ["dictionary","dictionaries"],
	b"\x0b": ["list of numbers","list of numbers"],
	b"\x0c": ["list of numbers","list of numbers"]
	}

def encode_string(string):
	return struct.pack('>H', len(string.encode('utf-8'))) + string.encode('utf-8')

def encode_int(integ, override = end):
	if -129 < integ < 128 and not override in [int16, int32, int64]:
		return (int8, encode_int8(integ))
	if -32769 < integ < 32768 and not override in [int32, int64]:
		return (int16, encode_int16(integ))
	elif -2147483649 < integ < 2147483648 and override != int64:
		return (int32, encode_int32(integ))
	elif -9223372036854775809 < integ < 9223372036854775808:
		return (int64, encode_int64(integ))
	else:
		raise TypeError("%s is too big" % integ)

def encode_int8(integ):
	return struct.pack('>b', integ)

def encode_uint8(integ):
	return struct.pack('>B', integ)

def encode_int16(integ):
	return struct.pack('>h', integ)

def encode_uint16(integ):
	return struct.pack('>H', integ)

def encode_int32(integ):
	return struct.pack('>i', integ)
	
def encode_uint32(integ):
	return struct.pack('>I', integ)
	
def encode_int64(integ):
	return struct.pack('>q', integ)
	
def encode_uint64(integ):
	return struct.pack('>Q', integ)

def encode_float(dec, override):
	if dec == struct.unpack('>f', struct.pack(">f", dec))[0] and override != float64:
		return (float32, struct.pack(">f", dec))
	else:
		return (float64, struct.pack(">d", dec))

def parse_json(data, override = end):
	if isinstance(data, list):
		if len(data) == 0 or not isinstance(data[0], tuple):
			tag = end
			special = end
			string = encode_uint32(len(data))
			for k, v in enumerate(data):
				tupel = parse_json(v)
				newtag = tupel[0]
				if isinstance(v, bool): # Boolian
					special = string16
				elif v == []: # Empty list
					special = list32
				elif tag != newtag:
					if tag == end and (special == end or special == list32 and newtag in [list32, int8_list32, int32_list32, int64_list32] or special == string16 and newtag in [int8, int16, int32, int64, string16]):
						tag = newtag
					elif tag in [float32, float64] and newtag in [float32,float64]:
						if tag == float32 and newtag == float64:
							tag = newtag
					elif tag in [list32, int8_list32, int32_list32, int64_list32] and newtag in [list32, int8_list32, int32_list32, int64_list32]:
						tag = list32
					elif tag in [int8, int16, int32, int64] and newtag in [int8, int16, int32, int64]:
						if newtag == int64 or (tag != int64  and (newtag == int32) or (tag != int32  and (newtag == int16) or (tag != int16  and (newtag == int8)))):
							tag = newtag
					else:
						raise TypeError("Found %s in a list of %s" % (mappings[newtag][0], mappings[tag][1]))      
			if tag == end and special != end:
				tag = special
			for k, v in enumerate(data):
				string += parse_json(v, tag)[1]
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
		else:
			string = b""
			for v in data[:-1]:
				value = parse_json(v)
				string += value
			return (object16, string + end)
	elif isinstance(data, tuple):
		key = encode_string(data[0])
		tupel = parse_json(data[1])
		tag = tupel[0]
		value = tupel[1]
		return tag + key + value
	elif isinstance(data, bool) and override in [end, string16]:
		return (string16, encode_string(str(data).lower()))
	elif isinstance(data, int):
		return encode_int(data, override)
	elif isinstance(data, float):
		return encode_float(data, override)
	elif isinstance(data, str):
		return (string16, encode_string(data))
	else:
		raise TypeError(type(data).__name__)

def conversion(inp,out):
	if os.path.isdir(inp):
		os.makedirs(out, exist_ok=True)
		for entry in sorted(os.listdir(inp)):
			conversion(os.path.join(inp, entry),os.path.join(out, entry))
	elif not inp.endswith('.' + 'rton'):
		split = os.path.splitext(out)[0]
		if split.endswith("hotbar"):
			extension = ".nbt"
		elif split.endswith("_mcr"):
			extension = ".dat_mcr"
			split = split.removesuffix('_mcr')  
		elif split.endswith("_old"):
			extension = ".dat_old"
			split = split.removesuffix('_old')  
		else:
			extension = ".dat"
		try:
			data=("", json.loads(open(inp, 'rb').read(), object_pairs_hook=parse_object_pairs))
		except:
			print("\nno json: %s" % inp)
		else:
			try:
				output = parse_json(data)
				write=split+extension
				if split.endswith(("servers","hotbar")):
					open(write, 'wb').write(output)
				else:
					gzip.open(write, 'wb').write(output)
				print("wrote " + write)
			except Exception as e:
				print('\n%s in %s: %s' % (type(e).__name__, inp, e))

def parse_object_pairs(pairs):
	pairs.append(("",""))
	return pairs

#fail=open("fail.txt","w")
#fail.write("fails:")
print("\033[95m\033[1mJSONSParser v1.0.0\n(C) 2021 by Nineteendo\033[0m\n")
try:
	inp = input("\033[1mInput file or directory:\033[0m ")
	out = input("\033[1mOutput directory:\033[0m ")
	if os.path.isfile(inp):
		out = os.path.join(out,os.path.basename(inp))
except:
	inp = "jsons/"
	out = "nbts/"
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
