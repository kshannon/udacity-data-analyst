#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kyle's code
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
    
    new_set = set()
    for n in FIELDS:
        fieldtypes[n] = new_set
        
    with open(CITIES, 'r') as csvfile:
        data_file = csv.DictReader(csvfile, delimiter=',')
        for i in range(3):
            data_file.next()
        for data in data_file:
            for name in FIELDS:
                if data[name]=='NULL' or data[name]=="":
                    #fieldtypes[name].add(type(None))
                    print "NONE | %s | %s | %s" % (data[name], fieldtypes[name], name)
                elif data[name].startswith("{") == True:
                    #fieldtypes[name].add(type([]))
                    print "LIST | %s | %s | %s" % (data[name], fieldtypes[name], name)
                elif int_check(data[name]) == True: # int function 1st
                    #fieldtypes[name].add(type(1))
                    print "INT | %s | %s | %s" % (data[name], fieldtypes[name], name)
                elif float_check(data[name]) == True:# float function 2nd
                    #fieldtypes[name] = fieldtypes[name].add(type(1.1))
                    print "FLOAT | %s | %s | %s" % (data[name], fieldtypes[name], name)
                else: 
                    fieldtypes[name] = fieldtypes[name].add(type("s"))
                    print "STR | %s | %s | %s" % (data[name], fieldtypes[name], name)
                
                for key in fieldtypes.keys():
                    print "the key name is: ", key, "and its value is: ", fieldtypes[key]
            
            print fieldtypes[name]
    #print fieldtypes
    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()


"""
Jon's code
"""


def isnone(value):
    return value == None or value == "" or value == "NULL"

def islist(value):
    return value != None and value.startswith("{")
    
def isint(value):
    try:
        int(value)
        return True
    except:
        return False
    
def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

def gettype(value):
    if isnone(value):
        return type(None)
    elif isint(value):
        return int
    elif isfloat(value):
        return float
    elif islist(value):
        return type([])
    else:
        return type("")


def audit_file(filename, fields):
    fieldtypes = {}
    with open(CITIES) as csvfile:
        data = csv.DictReader(csvfile, delimiter=',')
        for i in range(3):
            data.next()
        for row in data:
            for field in FIELDS:
                if (not field in fieldtypes):
                    fieldtypes[field] = set()
                fieldtypes[field].add(gettype(row[field]))