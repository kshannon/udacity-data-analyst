import pprint
from pymongo import MongoClient

client = MongoClient()
db = client.seattle_osm_database


print "size of collection: ", db.way_node_collection.count()

pprint.pprint(db.way_node_collection.find_one())
