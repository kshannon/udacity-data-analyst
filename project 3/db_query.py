import pprint
from pymongo import MongoClient


def make_pipeline():
	# complete the aggregation pipeline
	pipeline = [ {"$find": {"amenity": "bike"}}]
	return pipeline


def aggregate(db, pipeline):
	result = db.aggregate(pipeline)
	#pprint.pprint(result)
	return result


if __name__ == "__main__":
	# Initial local db setup
	client = MongoClient()
	db = client.seattle_osm_database.way_node_collection

	pipeline = make_pipeline()
	result = aggregate(db, pipeline)

	for document in result:
		pprint.pprint(document)


#print "size of collection: ", db.way_node_collection.count()

#pprint.pprint(db.way_node_collection.find_one())

# time min max
# Bike ammentiies
# relegion/church
# road types
# num of sources 
# look at shops/amenities. 

# Query for Min/Max 
# get all timestamps into a  list then sort them and 
# retrieve first and last entry