import pymongo

myclient = pymongo.MongoClient("mongodb+srv://chort:nurai2002@cluster0-8bmzm.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["pp2"]

#Find document(s) with the address "Park Lane 38":
myquery = { "address": "Park Lane 38" }

#Find documents where the address starts with the letter "S" or higher:
#myquery = { "address": { "$gt": "S" } }

#Find documents where the address starts with the letter "S":
#myquery = { "address": { "$regex": "^S" } }

mydoc = mycol.find(myquery)

for x in mydoc:
  print(x)