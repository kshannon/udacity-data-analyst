#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values
first.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]

def float_check(string):
    try:
        float(string)
        return True
    except:
        return False
    
def int_check(string):
    try:
        int(string)
        return True
    except:
        return False

def audit_file(filename, fields):
    fieldtypes = {}
    with open(CITIES, 'r') as csvfile:
        data_file = csv.DictReader(csvfile, delimiter=',')
        for i in range(3):
            data_file.next()
        for data in data_file:
            a_set = set()
            for name in FIELDS:
                if data[name]=='NULL' or data[name]=="":
                    fieldtypes[name] = a_set.add(type(None))
                elif data[name].startswith("{") == True:
                    fieldtypes[name] = a_set.add(type([]))
                elif int_check(data[name]) == True: # int function 1st
                    fieldtypes[name] = a_set.add(type(1.1))
                elif float_check(data[name]) == True:# float function 2nd
                    fieldtypes[name] = a_set.add(type(1))
                else: 
                    fieldtypes[name] = a_set.add(type("s"))
            print a_set
            fieldtypes[name] = a_set()
    print fieldtypes
    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
