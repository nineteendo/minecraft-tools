# JSON parser (ALPHA!)
# written by Nineteendo
# usage: put json files in jsons & run

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

mappings = {
	b"\x01": ["number","numbers"],
	b"\x02": ["number","numbers"],
	b"\x03": ["number","numbers"],
	b"\x04": ["number","numbers"],
	b"\x05": ["decimal number","decimal numbers"],
	b"\x06": ["decimal number","decimal numbers"],
	b"\x07": ["list of numbers","list of numbers"],
	b"\x08": ["string","strings"],
	b"\x09": ["list","lists"],
	b"\x0a": ["dictionary","dictionaries"],
	b"\x0b": ["list of numbers","list of numbers"],
	b"\x0c": ["list of numbers","list of numbers"]
	}

def encode_string(string):
	return struct.pack('>H', len(string.encode('utf-8'))) + string.encode('utf-8')

def encode_int(integ, override = End):
	if -129 < integ < 128 and not override in [Int16, Int32, Int64]:
		return (Int8, encode_int8(integ))
	if -32769 < integ < 32768 and not override in [Int32, Int64]:
		return (Int16, encode_int16(integ))
	elif -2147483649 < integ < 2147483648 and override != Int64:
		return (Int32, encode_int32(integ))
	elif -9223372036854775809 < integ < 9223372036854775808:
		return (Int64, encode_int64(integ))
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
	if dec == struct.unpack('>f', struct.pack(">f", dec))[0] and override != Double:
		return (Float, struct.pack(">f", dec))
	else:
		return (Double, struct.pack(">d", dec))

def parse_json(data, override = End):
	if isinstance(data, list):
		if len(data) == 0 or not isinstance(data[0], tuple):
			tag = End
			string = encode_uint32(len(data))
			for k, v in enumerate(data):
				tupel = parse_json(v)
				newtag = tupel[0]
				emptylist = newtag == List and tupel[1][:1] == End
				if tag != newtag and not emptylist:
					if tag == End:
						tag = newtag
					elif tag in [Float, Double] and newtag in [Float,Double]:
						if tag == Float and newtag == Double:
							tag = newtag
					elif tag in [List, Int8_List, Int32_List, Int64_List] and newtag in [List, Int8_List, Int32_List, Int64_List]:
						tag = List
					elif tag in [Int8, Int16, Int32, Int64] and newtag in [Int8, Int16, Int32, Int64]:
						if newtag == Int64 or (tag != Int64  and (newtag == Int32) or (tag != Int32  and (newtag == Int16) or (tag != Int16  and (newtag == Int8)))):
							tag = newtag
					else:
						raise TypeError("Found %s in a list of %s" % (mappings[newtag][0], mappings[tag][1]))      
			for k, v in enumerate(data):
				tupel = parse_json(v, tag)
				if tag == End:
					tag = tupel[0]
				value = tupel[1]
				string += value
			if override == List:
				return (List, tag + string)
			elif tag == Int8 or override == Int8_List:
				return (Int8_List, string)
			elif tag == Int32 or override == Int32_List:
				return (Int32_List, string)
			elif tag == Int64 or override == Int64_List:
				return (Int64_List, string)
			else:
				return (List, tag + string)
		else:
			string = b""
			for v in data[:-1]:
				value = parse_json(v)
				string += value
			return (Object, string + End)
	elif isinstance(data, tuple):
		key = encode_string(data[0])
		tupel = parse_json(data[1])
		tag = tupel[0]
		value = tupel[1]
		return tag + key + value
	elif isinstance(data, int):
		return encode_int(data, override)
	elif isinstance(data, float):
		return encode_float(data, override)
	elif isinstance(data, str):
		return (String, encode_string(data))
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
