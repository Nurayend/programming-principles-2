import pymongo

myclient = pymongo.MongoClient("mongodb+srv://chort:nurai2002@cluster0-8bmzm.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["pp2"]
#Delete the document with the address "Mountain 21":
myquery = { "address": "Mountain 21" }

#Delete all documents were the address starts with the letter S:
# myquery = { "address": {"$regex": "^S"} }
# x = mycol.delete_many(myquery)
# print(x.deleted_count, " documents deleted.")

#Delete all documents in the "customers" collection:
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")

mycol.delete_one(myquery)