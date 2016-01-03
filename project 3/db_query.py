import pprint
from pymongo import MongoClient


def make_pipeline():
	# complete the aggregation pipeline
	pipeline = [ 
			#{'$match' : {'user' : 1}},
			{'$group' : {'_id' : '$user',
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

	print ("number of nodes: %d and number of ways: %d" 
				%(db.count({'type' : 'node'}),
				db.count({'type' : 'way'})))

	#return the number of documents in db
	print 'Number of documents in db: ', db.find().count()

	#return the num of unique users
	print 'Unique Users: ', db.distinct({'created.user'}).length

	print "Saved by the "


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


# SOURCE INFO:
	# Unique source counts:
			# pipeline = [ 
			# 		{'$group' : {'_id' : '$source',
		 #                            'count' : {'$sum' : 1 }}},
		 #            {'$sort' : {'count' : -1}},
		 #            {'$limit' : 20}
			# ]
	# returns:
					# {u'_id': None, u'count': 6917511}
					# {u'_id': u'King County GIS;data.seattle.gov', u'count': 183167}
					# {u'_id': u'data.seattle.gov', u'count': 56847}
					# {u'_id': u'Bing', u'count': 39542}
					# {u'_id': u'US-NPS_import_b2a6c900-5dcc-11de-8509-001e2a3ffcd7',
					#  u'count': 31998}
					# {u'_id': u'King County GIS', u'count': 30752}
					# {u'_id': u'http://www.fs.fed.us/r6/data-library/gis/olympic/hydronet_meta.htm',
					#  u'count': 30479}
					# {u'_id': u'PGS', u'count': 21490}
					# {u'_id': u'NRCan-CanVec-10.0', u'count': 13165}
					# {u'_id': u'yahoo_wms', u'count': 12371}
					# {u'_id': u'bing', u'count': 11669}
					# {u'_id': u'NRCan-CanVec-8.0', u'count': 5460}
					# {u'_id': u'US-NFS', u'count': 3952}
					# {u'_id': u'SDOT Bike Rack Import 2012', u'count': 2481}
					# {u'_id': u'TIGER/Line\xae 2008 Place Shapefiles (http://www.census.gov/geo/www/tiger/)',
					#  u'count': 1146}
					# {u'_id': u'Yahoo', u'count': 996}
					# {u'_id': u'data.seattle.gov;King County GIS', u'count': 994}
					# {u'_id': u'Garmin Forerunner 305', u'count': 985}
					# {u'_id': u'Geobase_Import_2009', u'count': 909}
					# {u'_id': u'tiger_import_20070610', u'count': 835}




# time min max
# relegion/church
# road types
# num of sources 
# look at shops/amenities. 

# Query for Min/Max 
# get all timestamps into a  list then sort them and 
# retrieve first and last entry