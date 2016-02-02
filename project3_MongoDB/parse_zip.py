import re

postcode = re.compile(r'\d{5}')

zip_strs = ['98466', 
		'98409-6483', 
		'98424-1915', 
		'98424', 
		'98408', 
		'98391-6301', 
		'98408-1240', 
		'98103', 
		'98003', 
		'98003-5402', 
		'98531', 
		'V8V 3M8', 
		'V9C 2V9', 
		'98501', 
		'V8X3W6', 
		'W Lake Sammamish Pkwy NE', 
		'Olympia, 98502', 
		'Olympia, 98502', 
		'Olympia, 98502', 
		'Olympia, WA 98502', 
		'Lacey, 98503']

def parse_zip(data):	
	return ''.join(postcode.findall(data))
	
for zip in zip_strs:
	print 'input: %s, postcode: %s' % (zip, parse_zip(zip))
	
