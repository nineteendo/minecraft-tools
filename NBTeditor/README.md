# NBTeditor
## Usage
* Put NBT files in folder, run parse.py and insert input path and output path to your file or folder
* Edit files as JSON
* run encode.py and insert input path and output path

# Options.json
key | default | purpose
--- | --- | ---
AllowNan | true | Allow NaN, -infinity and infinity as values
AutoBool | true | Convert "true" and "false" to bool
AutoFloat | false | Automatically convert number to decimal number
AutoInt | false | Automatically convert decimal number to number
BigEndian | null | Convert to Java Edition or Bedrock Edition
CommaSeparator | "" | Separator between values
DEBUG_MODE | false | crash program on error with all information
DoublePointSeparator | " " | Separator between key and value
EnsureAscii | false | escape non-ASCII characters
Indent | "\t" | null, number of spaces or text as indent
NBTExtensions | [".dat", ".dat_mcr", ".dat_old", ".mcstructure", ".nbt"] | Extensions of NBT files
RepairFiles | true | Repair NBT files that end abruptly
SortKeys | false | Sort keys in dictionary
UncompressedFiles | ["_BE", ".mcstructure", ".nbt", "/servers.dat", "/servers.dat_old"] | Files that are not compressed

# NBT format
Bytecode | Type | Name | Limitations
--- | --- | --- | ---
`0x0` | end | TAG_End | Object End / Empty list type
`0x1` | int8 | TAG_Byte | -128 to 127
`0x2` | int16 | TAG_Short | -32768 to 32767
`0x3` | int32 | TAG_Int | -2147483648 to 2147483647
`0x4` | int64 | TAG_Long | -9223372036854775808 to 9223372036854775807
`0x5` | float32 | TAG_Float | Single-precision floating-point
`0x6` | float64 | TAG_Double | Double-precision floating-point
`0x7` | int8_list32 | TAG_Byte_Array | 0-2147483647 elements
`0x8` | string16 | TAG_String | 0-65535 characters
`0x9` | list32| TAG_List | 0-2147483647 elements
`0xa` | object16 | TAG_Compound | 0-512 depth
`0xb` | int32_list32 | TAG_Int_Array | 0-2147483647 elements
`0xc` | int64_list32 | TAG_Long_Array | 0-2147483647 elements

## Numbers
### `0x1`
* `0x1 xxxx [string] yy` creates a `[string]` with `xxxx` uint16 of bytes with `yy` int8 as value
* Example:
	```NBT
    01 00 06 68 65 61 6C 74 68 05
    ```
* JSON Decode:
	```JSON
    {
    	"health": 5
    }
	```
### `0x2`
* `0x2 xxxx [string] yyyy` creates a `[string]` with `xxxx` uint16 of bytes with `yyyy` int16 as value
* Example:
	```NBT
    02 00 06 62 6C 6F 63 6B 73 30 31
    ```
* JSON Decode:
	```JSON
    {
    	"blocks": 12337
    }
	```
### `0x3`
* `0x3 xxxx [string] yyyyyyyy` creates a `[string]` with `xxxx` uint16 of bytes with `yyyyyyyy` int32 as value
* Example:
	```NBT
    03 00 07 76 65 72 73 69 6F 6E 00 02 82 B3
    ```
* JSON Decode:
	```JSON
    {
    	"version": 164531
    }
	```
### `0x4`
* `0x4 xxxx [string] yyyyyyyyyyyyyyyy` creates a `[string]` with `xxxx` uint16 of bytes with `yyyyyyyyyyyyyyyy` int64 as value
* Example:
	```NBT
    04 00 04 74 69 6D 65 00 00 00 18 FF E1 0A 82
    ```
* JSON Decode:
	```JSON
    {
    	"time": 107372153474
    }
	```
## Decimal Numbers
### `0x5`
* `0x5 xxxx [string] yyyyyyyy` creates a `[string]` with `xxxx` uint16 of bytes with `yyyyyyyy` float32 as value
* Example:
	```NBT
    05 00 01 78 3F 82 EF F5
    ```
* JSON Decode:
	```JSON
    {
    	"x": 1.022947907447815
    }
	```
### `0x6`
* `0x6 xxxx [string] yyyyyyyyyyyyyyyy` creates a `[string]` with `xxxx` uint16 of bytes with `yyyyyyyyyyyyyyyy` float64 as value
* Example:
	```NBT
    06 00 01 78 40 21 90 44 72 91 3B 28
    ```
* JSON Decode:
	```JSON
    {
    	"x": 8.7817722132
    }
	```
## Number Lists
### `0x7`
* `0x7 xxxx [string] 0x7` creates a `[string]` with `xxxx` uint16 of bytes with a list of int8 as value
* List begins with int32 of elements
* Example:
    ```
    07 00 09 69 6E 76 65 6E 74 6F 72 79
    00 00 00 02
    	01
    	7F
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			1,
			127
		]
	}
    ```
### `0xB`
* `0xB xxxx [string] 0xB` creates a `[string]` with `xxxx` uint16 of bytes with a list of int32 as value
* List begins with int32 of elements
* Example:
    ```
    0B 00 09 69 6E 76 65 6E 74 6F 72 79
    00 00 00 02
    	00 00 00 80
    	00 01 F5 C5
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			128,
			128453
		]
	}
    ```
### `0xc`
* `0xC xxxx [string] 0xC` creates a `[string]` with `xxxx` uint16 of bytes with a list of int64 as value
* List begins with int32 of elements
* Example:
    ```
    0C 00 09 69 6E 76 65 6E 74 6F 72 79
    00 00 00 02
    	00 00 00 00 00 00 02 1F
    	00 00 00 01 40 9E ED 8B
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			543,
			5379124619
		]
	}
    ```
### String
## `0x8`
* `0x8 xxxx [string] yyyy [string 2]` creates a `[string]` with `xxxx` uint16 of bytes with a `[string 2]` with `yyyy` uint16 of bytes as value
* Example:
    ```
    08 00 04 6E 61 6D 65 00 09 42 61 6E 61 6E 72 61 6D 61
    ```
* JSON Decode
    ```JSON
    {
    	"name": "Bananrama"
    }
    ```
### List
#### `0x9`
* `0x9 xxxx [string]` creates a `[string]` with `xxxx` uint16 of bytes with a list as value
* It has 13 subsets (`0x0`, `0x1`, `0x2`, `0x3`, `0x4`, `0x5`, `0x6`, `0x7`, `0x8`, `0x9`, `0xa`, `0xb`, `0xc`)

#### `0x0` Subset
* `0x9 xxxx [string] 0x0` creates a `[string]` with `xxxx` uint16 of bytes with an empty list as value
* Example:
	```NBT
	09 00 09 69 6E 76 65 6E 74 6F 72 79
	00
    00 00 00 00
    ```
* JSON Decode
    ```JSON
    {
    	"inventory": []
    }
    ```
#### `0x1` Subset
* `0x9 xxxx [string] 0x1` creates a `[string]` with `xxxx` uint16 of bytes with a list of int8 as value
* Example:
	```NBT
    09 00 09 69 6E 76 65 6E 74 6F 72 79
    01
    00 00 00 02
    	01
    	7F
    ```
* JSON Decode
    ```JSON
    {
    	"inventory": [
    		1,
    		127
    	]
    }
    ```
#### `0x2` Subset
* `0x9 xxxx [string] 0x2` creates a `[string]` with `xxxx` uint16 of bytes with a list of int16 as value
* Example:
	```NBT
    09 00 09 69 6E 76 65 6E 74 6F 72 79
    02
    00 00 00 02
    	00 01
    	01 E3
    ```
* JSON Decode
    ```JSON
    {
    	"inventory": [
    		1,
    		483
    	]
    }
    ```
#### `0x3` Subset
* `0x9 xxxx [string] 0x3` creates a `[string]` with `xxxx` uint16 of bytes with a list of int32 as value
* Example:
	```NBT
    09 00 09 69 6E 76 65 6E 74 6F 72 79
    03
    00 00 00 02
    	00 00 00 80
    	00 01 F5 C5
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			128,
			128453
		]
	}
    ```
#### `0x4 Subset
* `0x9 xxxx [string] 0x4` creates a `[string]` with `xxxx` uint16 of bytes with a list of int64 as value
* Example:
	```NBT
    09 00 09 69 6E 76 65 6E 74 6F 72 79
    04
    00 00 00 02
    	00 00 00 00 00 00 02 1F
    	00 00 00 01 40 9E ED 8B
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			543,
			5379124619
		]
	}
    ```
#### `0x5 Subset
* `0x9 xxxx [string] 0x5` creates a `[string]` with `xxxx` uint16 of bytes with a list of float32 as value
* Example:
	```NBT
    09 00 09 69 6E 76 65 6E 74 6F 72 79
    05
    00 00 00 02
    	3F 80 00 00
    	41 0C 82 24
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			1.0,
			8.78177261352539
		]
	}
    ```
#### `0x6 Subset
* `0x9 xxxx [string] 0x6` creates a `[string]` with `xxxx` uint16 of bytes with a list of float64 as value
* Example:
	```NBT
    09 00 09 69 6E 76 65 6E 74 6F 72 79
    06
    00 00 00 02
    	3F F1 99 99 99 99 99 9A
    	3F F0 B0 20 C4 9B A5 E3
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			1.1,
			1.043
		]
	}
    ```
#### `0x7 Subset
* `0x9 xxxx [string] 0x6` creates a `[string]` with `xxxx` uint16 of bytes with a list of lists of int8 as value
* Example:
	```NBT
	09 00 09 69 6E 76 65 6E 74 6F 72 79
	07
	00 00 00 03
		00 00 00 00
		00 00 00 02
			01
			11
		00 00 00 02
			02
			3A
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			[],
			[
				1,
				17
			],
			[
				2,
				58
			]
		]
	}
    ```
#### `0x8` Subset
* `0x9 xxxx [string]` creates a `[string]` with `xxxx` uint16 of bytes with an list of string16 as value
* Example:
    ```
	09 00 09 69 6E 76 65 6E 74 6F 72 79
	08
	00 00 00 02
		00 05 62 72 65 61 64
		00 05 61 70 70 6C 65
    ```
* JSON Decode
    ```JSON
    {
    	"inventory": [
    		"bread",
    		"apple"
    	]
    }
    ```
#### `0x9` Subset
* `0x9 xxxx [string] 0x6` creates a `[string]` with `xxxx` uint16 of bytes with a list of lists as value
* Example:
	```NBT
	09 00 09 69 6E 76 65 6E 74 6F 72 79
	09
	00 00 00 02
		01
			00 00 00 02
				01
				11
		02
			00 00 00 02
				00 02
				00 80
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			[
				1,
				17
			],
			[
				2,
				128
			]
		]
	}
    ```
#### `0xA`Subset
* `0x9 xxxx [string] 0xA` creates a `[string]` with `xxxx` uint16 of bytes with a list of objects as value
* Example:
	```NBT
	09 00 09 69 6E 76 65 6E 74 6F 72 79
	0A
	00 00 00 02
	00
		08 00 04 73 69 67 6e 00 04 74 65 78 74
	00
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			{},
			{
				"sign": "text"
			}
			
		]
	}
    ```
#### `0xB`Subset
* `0x9 xxxx [string] 0xB` creates a `[string]` with `xxxx` uint16 of bytes with a list of lists of int32 as value
* Example:
	```NBT
	09 00 09 69 6E 76 65 6E 74 6F 72 79
	0B
	00 00 00 02
		00 00 00 02
			00 00 00 80
			00 01 F5 C5
		00 00 00 02
			00 00 00 2B
			00 01 31 57	
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			[
				128,
				128453
			],
			[
				43,
				78167
			]
			
		]
	}
    ```
#### `0xC`Subset
* `0x9 xxxx [string] 0xC` creates a `[string]` with `xxxx` uint16 of bytes with a list of lists of int64 as value
* Example:
	```NBT
	09 00 09 69 6E 76 65 6E 74 6F 72 79
	0C
	00 00 00 02
		00 00 00 02
			00 00 00 00 00 00 02 1F
			00 00 00 01 40 9E ED 8B
		00 00 00 02
			00 00 00 00 00 00 05 FC
			00 00 00 02 32 68 FB 2F
    ```
* JSON Decode
    ```JSON
    {
		"inventory": [
			[
				543,
				5379124619
			],
			[
				1532,
				9435675439
			]
			
		]
	}
    ```
### `0xA`
* `0x85 xxxx [string]` creates a `[string]` with `xxxx` uint16 of bytes with an object as value
* Example:
    ```
	0A 00 04 54 65 73 74
		08 00 04 6E 61 6D 65 00 09 42 61 6E 61 6E 72 61 6D 61
		08 00 07 4D 65 73 73 61 67 65 00 0B 48 65 6C 6C 6F 20 57 6F 72 6C 64
	00
    ```
* JSON Decode
    ```JSON
    {
    	"Test": {
    		"name": "Bananrama",
    		"Message": "Hello World"
    	}
    }
    ```
### `0x0`
* `0x0` marks end of an object
* Example:
    ```
    0A 00 00
    00
    ```
* JSON Decode
    ```JSON
    {}
    ```