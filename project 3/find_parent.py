# ==================================================
# Find which parent node tag has children with a 
# value of k specified
# ==================================================

# find which node parent type has keys containing the string 'tiger'

import xml.etree.cElementTree as ET
import re
import pprint
from sys import argv

tag_feature = re.compile(r'k="[\w:]+')
tags = set()

if (len(argv) != 3):
	exit(str.format('usage: python {0} k-value filename', argv[0]))

script_name, key_value, filename = argv
	
def find_keys(element):
	if element.tag in ['node', 'way']:
		for child in element:
			if 'k' in child.attrib:
				if key_value in child.attrib['k']:
				#if 'tiger' in child.attrib['k']:
					tags.add(element.tag)
					#print element.tag
					#tags.add(child.attrib['k'])
				#print child.attrib['k']
			
	

with open(filename) as file:
	for _, element in ET.iterparse(file):
		#print find_keys(element)
		find_keys(element)
		
pprint.pprint(tags)

# send a bell character to console to let us know the script has finished
print('')