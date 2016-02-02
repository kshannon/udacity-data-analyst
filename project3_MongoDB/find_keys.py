# ==================================================
# Find all values for attribute k in child elements 
# of 'node' and 'way' elements in an OSM document.
# ==================================================

import xml.etree.cElementTree as ET
import re
import pprint
from sys import argv

# make sure the user has provided us with a filename argument
# the length of argv must be 2 because the first item is the
# name of the script, so the argument is the second item.
if (len(argv) != 2):
	exit(str.format('usage: python {0} filename', argv[0]))
	
script_name, filename = argv

# this regex finds values for the key attribute by 
# matching alphanumeric characters following k="
# e.g.:
# <tag k="enabled" v="yes"/>						=> enabled
# <tag k="addr:street" v="West Lexington St."/>		=> addr:street	
# <tag k="addr:street:prefix" v="West"/>			=> addr:street:prefix
# <tag k="chicago:building_id" v="366409"/>			=> chicago:building_id
tag_feature = re.compile(r'k="[\w:]+')
tags = set() 	

def find_keys(element):
	if element.tag in ['node', 'way']:
		for child in element:
			if 'k' in child.attrib:
				tags.add(child.attrib['k'])

with open(filename) as file:
	for _, element in ET.iterparse(file):
		find_keys(element)
		
pprint.pprint(tags)

# send a bell character to console to let us know the script has finished
print('')