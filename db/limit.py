import pymongo

myclient = pymongo.MongoClient("mongodb+srv://chort:nurai2002@cluster0-8bmzm.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["pp2"]
#Limit the result to only return 5 documents:
myresult = mycol.find().limit(5)
for x in myresult:
  print(x)