# ==================================================
# Count values inside 'node' or 'way' nodes for attribute 
# 'v' under attribute 'k' having the value specified
# ==================================================


import xml.etree.cElementTree as ET
import re
import pprint
from sys import argv

tag_feature = re.compile(r'k="[\w:]+')
values = {}

if (len(argv) != 3):
	exit(str.format('usage: python {0} key filename', argv[0]))

script_name, key_value, filename = argv
	
def find_values(element):
	if element.tag in ['node', 'way']:
		for child in element:
			if 'k' in child.attrib:
				if key_value == child.attrib['k']:
					val = child.attrib['v']
					if val in values:
						values[val] += 1
					else:
						values[val] = 1

with open(filename) as file:
	for _, element in ET.iterparse(file):
		find_values(element)
		
pprint.pprint(values)

# send a bell character to console to let us know the script has finished
print('')