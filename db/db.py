import pymongo

myclient = pymongo.MongoClient("mongodb+srv://chort:nurai2002@cluster0-8bmzm.mongodb.net/test?retryWrites=true&w=majority")

mydb = myclient["pp2"]
print(myclient.list_database_names())
#dblist = myclient.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")