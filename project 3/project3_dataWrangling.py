#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# global list containing keys to be used in dictinary
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_data(element):
    data_element = {}
    # choosing not to include "relation" top level tag
    if element.tag in ["node", "way"]:
        created = {}
        pos = [0,0]
        data_element['type'] = element.tag
        
        for k, v in element.attrib.iteritems():
            #print k, v
            if k in CREATED:
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
                                           
        return data_element




def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_data(element)
            if el:
                data.append(el)
    return data

file_in = "sample_seattle.osm"
process_map(file_in)



