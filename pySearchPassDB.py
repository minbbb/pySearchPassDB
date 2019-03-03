import pymongo
import os
import re
import sys
import argparse

coll = pymongo.MongoClient("localhost", 27017)["db"]["collection"]
patternSplit = r':'

#Add fields to db
def addToDB(dir):
	countPass = 0
	countEmail = 0
	for files in os.walk(dir):
		for file in files[2]:
			with open(files[0] + "/" + file) as f:
				for line in f:
					arrLine = re.split(patternSplit, line, maxsplit=1)
					arrLine[0] = arrLine[0].lower()
					if coll.find({"email": arrLine[0]}).count() == 0:
						coll.save({"email": arrLine[0], "pass": [arrLine[1]]})
						countEmail += 1
						countPass += 1
					else:
						if not arrLine[1] in coll.find_one({"email": arrLine[0]})["pass"]:
							coll.update_one({"email": arrLine[0]}, { '$push': { "pass": arrLine[1]} })
							countPass += 1
	print("Added " + str(countEmail) + " emails\nand " + str(countPass) + " passwords")

#Clear all db fields
def clearDB():
	coll.remove({})

#Search email
def searchEmail(email):
	return coll.find_one({"email": email})

#Search email and convenient output
def printSearchEmail(email):
	res = searchEmail(email)
	if res:
		print("email:" + res["email"])
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
