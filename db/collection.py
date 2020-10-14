import pymongo

myclient = pymongo.MongoClient("mongodb+srv://chort:nurai2002@cluster0-8bmzm.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]

mycol = mydb["pp2"]
#print(mydb.list_collection_names())
collist = mydb.list_collection_names()
if "customers" in collist:
  print("The collection exists.")