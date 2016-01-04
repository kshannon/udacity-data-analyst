import xml.etree.cElementTree as ET
import pprint


def get_user(element):
    return element.get('uid')

def unique_users(filename):
    users = set()
    count = 0
    for _, element in ET.iterparse(filename):
        if get_user(element) == None:
            continue
        users.add(get_user(element))
    print len(users)

xml_file = "sample_seattle.osm"
unique_users(xml_file)