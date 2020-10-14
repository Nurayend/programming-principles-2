import pymongo

myclient = pymongo.MongoClient("mongodb+srv://chort:nurai2002@cluster0-8bmzm.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["pp2"]

#Sort the result alphabetically by name:
mydoc = mycol.find().sort("name")

#Sort the result reverse alphabetically by name:
#mydoc = mycol.find().sort("name", -1)

for x in mydoc:
  print(x)