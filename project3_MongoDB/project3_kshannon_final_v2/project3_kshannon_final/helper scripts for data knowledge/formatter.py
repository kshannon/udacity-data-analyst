from sys import argv

script_name, abbr, new_name = argv

print '"{0}" : "{1}",'.format(abbr, new_name)
print '"{0}." : "{1}",'.format(abbr, new_name)