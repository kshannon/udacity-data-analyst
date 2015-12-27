import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
        # YOUR CODE HERE
        tags = {}
        for event, elem in ET.iterparse(filename):
            #print elem.tag
            if elem.tag in tags:
                tags[elem.tag] += 1
            else:
                tags[elem.tag] = 1
        print tags


xml_file = "sample_seattle.osm"
count_tags(xml_file)