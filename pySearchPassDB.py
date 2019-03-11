import pymongo
import os
import re
import sys
import argparse

coll = pymongo.MongoClient("localhost", 27017)["pySearchPassDB"]["pySearchPassDB"]
PATTERN_SPLIT = (':', ';')

#Add fields to db
def addToDB(dir):
	for files in os.walk(dir):
		for file in files[2]:
			with open(files[0] + "/" + file, errors='ignore') as f:
				for line in f:
					for pattern in PATTERN_SPLIT:
						arrLine = re.split(pattern, line.strip('\n'), maxsplit=1)
						if len(arrLine) == 2:
							break
					else:
						print("Error: string '" + str(arrLine[0].strip('\n')) + "' does not parse")
						continue
					arrLine[0] = arrLine[0].lower()
					coll.update({"_id": arrLine[0]}, { '$addToSet': { "pass": arrLine[1]} }, upsert=True)

#Clear all db fields
def clearDB():
	coll.remove({})

#Search email
def searchEmail(email):
	return coll.find_one({"_id": email.lower()})

#Search email and convenient output
def printSearchEmail(email):
	res = searchEmail(email)
	if res:
		print("email:" + res["_id"])
		if len(res["pass"]) > 1:
			print("passwords:")
			for p in res["pass"]:
				print(p)
		else:
			print("password:" + res["pass"][0])
	else:
		print("Not found")

#Get count fileds of db
def getCountEmails():
	return coll.count()

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--search', help='Search email', metavar = 'EMAIL')
parser.add_argument('-a', '--add', help='Add fields to db', metavar = 'PATH')
parser.add_argument('-c', '--count', action='store_true', help='Show count fileds of db')
parser.add_argument('--clear', action='store_true', help='Clear all db fields')

if parser.parse_args().count:
	print(getCountEmails())

if parser.parse_args().search:
	printSearchEmail(parser.parse_args().search)

if parser.parse_args().clear:
	clearDB()

if parser.parse_args().add:
	addToDB(parser.parse_args().add)

if len(sys.argv) == 1:
	parser.print_help()
