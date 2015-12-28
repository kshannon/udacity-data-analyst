#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.seattle_osm_database

way_node_collection = db.way_node_collection


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
postcode = re.compile(r'\d{5}')



# takes key/value from element.attrib.iteritems(). data from k/v is parsed into a created 
# dict and pos list. Both dict and list are added as values into the data_element dictionary.
def created_tags(k, v, data_element, created, pos):
    created_check_list = [ "version", "changeset", "timestamp", "user", "uid"]
    if k in created_check_list:
        created[k] = v
    else:
        if k == "lat":
            pos[0] = float(v)
        elif k == "lon":
            pos[1] = float(v)
        else:
            data_element[k] = v    
    data_element['created'] = created
    data_element['pos'] = pos
    return data_element


def shape_data(element):
    data_flag = True
    data_element = {}
    # choosing not to include "relation" top level tag
    if element.tag in ["node", "way"]:
        created = {}
        pos = [0,0]
        data_element['type'] = element.tag
        
        for k, v in element.attrib.iteritems():
            # function to return data_element with k/v for {created : dict} and {pos : list[]}
            created_tags(k, v, data_element, created, pos) # function for creted dict
            
            address = {}
            node_refs = []
            for child in element:
                if 'ref' in child.attrib:
                    node_refs.append(child.attrib['ref'])
                    continue
                else:
                    #print child.attrib['k']
                    if child.attrib['k'].startswith('addr:'):
                        if ':' in child.attrib['k'][5:]:
                            continue

                        address[child.attrib['k'].replace('addr:', '')] = child.attrib['v']
                data_element['node_refs'] = node_refs
                data_element['address'] = address        
                                           
        if data_flag == True:
            print data_element
        else:
            print "no"


def process_osm(file_in):
	with open(file_in) as file:
		for _, element in ET.iterparse(file):
			el = shape_data(element)
			if el:
				way_node_collection.insert(el)

if __name__ == "__main__":
    process_osm('example.osm')


# def parse_zip(data):    
#     return ''.join(postcode.findall(data))
    
# for zip in zip_strs:
#     print 'input: %s, postcode: %s' % (zip, parse_zip(zip))



