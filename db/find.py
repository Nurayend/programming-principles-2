import pymongo

myclient = pymongo.MongoClient("mongodb+srv://chort:nurai2002@cluster0-8bmzm.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["pp2"]

#Find the first document in the customers collection:
x = mycol.find_one()
print(x)

#Return all documents in the "customers" collection, and print each document
for x in mycol.find():
  print(x)

#Return only the names and addresses, not the _ids
for x in mycol.find({},{ "_id": 0, "name": 1, "address": 1 }):
  print(x)