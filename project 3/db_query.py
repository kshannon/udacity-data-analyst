import pprint
from pymongo import MongoClient



def make_pipeline():
	# complete the aggregation pipeline
	pipeline = [ 
			{'$match' : {'amenity' : 'restaurant'}},
			{'$group' : {'_id' : '$cuisine',
                            'count' : {'$sum' : 1 }}},
            {'$sort' : {'count' : -1}},
            {'$limit' : 20}

	]
	

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
	#result = db.find()

	for document in result:
		pprint.pprint(document)
	print ""


#print "size of collection: ", db.way_node_collection.count()

#pprint.pprint(db.way_node_collection.find_one())


# OVERALL DB INFORMATION:

	# this gets me an ordered list of unique amenity value counts.
				# pipeline = [ 
				# 		#{"$match": {"amenity": "bicycle_parking"}},
				# 		{'$group' : {'_id' : '$amenity',
			 	#                        'count' : {'$sum' : 1 }}},
			 	#           {'$sort' : {'count' : -1}},
				# ]
 
 		# returns:
				# {u'_id': None, u'count': 7348290}
				# {u'_id': u'parking', u'count': 7860}
				# {u'_id': u'bicycle_parking', u'count': 3059}
				# ...

	# Top 25 active users:
				# pipeline = [ 
				# 		{'$group' : {'_id' : '$created.user',
			 	#                   'count' : {'$sum' : 1 }}},
			 	#       {'$sort' : {'count' : -1}},
			 	#       {'$limit' : 25}
				# ]
		# returns:
				# {u'_id': u'Glassman', u'count': 1217504}
				# {u'_id': u'SeattleImport', u'count': 749345}
				# {u'_id': u'tylerritchie', u'count': 667752}
				# {u'_id': u'woodpeck_fixbot', u'count': 634558}
				# {u'_id': u'alester', u'count': 311665}

	# Top 20 appearing amenities:
				# pipeline = [ 
				# 		{'$match' : {'amenity' : {'$exists' : 1}}},
				# 		{'$group' : {'_id' : '$amenity',
			    #                         'count' : {'$sum' : 1 }}},
			    #        {'$sort' : {'count' : -1}},
			    #        {'$limit' : 20}
				# ]
		# Returns:
				# {u'_id': u'parking', u'count': 7860}
				# {u'_id': u'bicycle_parking', u'count': 3059}
				# {u'_id': u'school', u'count': 2520}
				# {u'_id': u'restaurant', u'count': 2257}
				# {u'_id': u'bench', u'count': 1713}
				# {u'_id': u'place_of_worship', u'count': 1345}
				# {u'_id': u'fast_food', u'count': 992}
				# {u'_id': u'cafe', u'count': 947}
				# {u'_id': u'fuel', u'count': 850}
				# {u'_id': u'toilets', u'count': 754}
				# {u'_id': u'waste_basket', u'count': 751}

	# get the count for ways and nodes:
			
					# pipeline = [ {'$group' : {'_id' : '$type',
		           #                 'count' : {'$sum' : 1 }}},
		           #  {'$sort' : {'count' : -1}},
		           #  {'$limit' : 20}]

		# Returns:		
				# {u'_id': u'node', u'count': 6762600}
				# {u'_id': u'way', u'count': 614082}

# BIKE AMENITIES:
				# grep -c bicycle_parking seattle_washington.osm --> =3210 count
				# grep -e bicycle seattle_washington.osm --> this got me the name of the tags:
			# <tag k="bicycle" v="yes"/> or v="no", v="designated", v="private", v="limited", v="permissive"/>
			# <tag k="shop" v="bicycle"/>
			# <tag k="amenity" v="bicycle_parking"/>
			# <tag k="route" v="bicycle"/>
			# <tag k="except" v="bicycle"/>

	# return ordered list of users that added bike amenity info:
				# pipeline = [ 
				# 			{"$match": {"amenity": "bicycle_parking"}},
				# 			{'$group' : {'_id' : '$created.user',
				#                             'count' : {'$sum' : 1 }}},
				#                {'$sort' : {'count' : -1}},
				# 	]
			
	# returns:
				# {u'_id': u'WBSKI', u'count': 2279}
				# {u'_id': u'zephyr', u'count': 166}
				# {u'_id': u'seattlefyi', u'count': 90}
				# ...



# FOOD:

	#checking out unique cusines by count:
				# pipeline = [ 
				# 		{'$match' : {'amenity' : 'restaurant'}},
				# 		{'$group' : {'_id' : '$cuisine',
			 #                            'count' : {'$sum' : 1 }}},
			 #            {'$sort' : {'count' : -1}},
			 #            {'$limit' : 20}

				# ]
		# Returns:

					# {u'_id': None, u'count': 825}
					# {u'_id': u'mexican', u'count': 163}
					# {u'_id': u'pizza', u'count': 160}
					# {u'_id': u'american', u'count': 120}
					# {u'_id': u'chinese', u'count': 105}
					# {u'_id': u'thai', u'count': 100}
					# {u'_id': u'asian', u'count': 86}
					# {u'_id': u'italian', u'count': 83}
					# {u'_id': u'japanese', u'count': 77}
					# {u'_id': u'sandwich', u'count': 56}
					# {u'_id': u'vietnamese', u'count': 53}
					# {u'_id': u'seafood', u'count': 43}

# time min max
# relegion/church
# road types
# num of sources 
# look at shops/amenities. 

# Query for Min/Max 
# get all timestamps into a  list then sort them and 
# retrieve first and last entry