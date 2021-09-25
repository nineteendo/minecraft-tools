import os, json, struct, gzip

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
	result = []
	for i in range(parse_int32(fp)):
		result.append(parse_int8(fp))
	
def parse_string(fp):
	return fp.read(struct.unpack('>H', fp.read(2))[0]).decode('utf-8')
	
def parse_list(fp):
	result = []
	code = fp.read(1)
	lenght = parse_int32(fp)
	if code == b"\x00":
		return result
	if code in mappings:
		for i in range(lenght):
			result.append(mappings[code](fp))
	return result
	
def parse_int32_array(fp):
	result = []
	for i in range(parse_int32(fp)):
		result.append(parse_int32(fp))
	return result
	
def parse_int64_array(fp):
	result = []
	for i in range(parse_int32(fp)):
		result.append(parse_int64(fp))
	return result
	
def parse_compound(fp):
	result = {}

	try:
		while True:
			tuple = parse(fp)
			result[tuple[0]] = tuple[-1]
	except KeyError as k:
		if k.args[0] == b'':
			fail.write("\n	SilentError: %s pos %s: End of file" %(fp.name,fp.tell()-1))
		else:
			raise k
	except StopIteration:
		pass
	
	return result

def parse(fp):
	code = fp.read(1)
	if code == b"\x00":
		raise StopIteration
	return (parse_string(fp), mappings[code](fp))

def conversion(inp,out):
	if os.path.isdir(inp):
		os.makedirs(out, exist_ok=True)
		for entry in sorted(os.listdir(inp)):
			conversion(os.path.join(inp, entry),os.path.join(out, entry))
	elif not inp.endswith('.' + 'json'):
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
			fail.write('\n' + str(type(e).__name__) + ': ' + inp + ' pos {0}: '.format(file.tell()-1)+str(e))

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

fail=open("fail.txt","w")
fail.write("fails:")
conversion("nbts","jsons")
fail.close()
try:
	os.startfile("fail.txt")
except:
	try:
		os.system("open fail.txt")
	except:
		os.system("xdg-open fail.txt")