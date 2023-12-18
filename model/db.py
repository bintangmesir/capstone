from . import *

USERNAME = os.getenv("DATABASE_USERNAME")
PASSWORD = os.getenv("DATABASE_PASSWORD")
cluster = MongoClient(
    f'mongodb://{USERNAME}:{PASSWORD}@ac-wy0xado-shard-00-00.o5uq1c1.mongodb.net:27017,ac-wy0xado-shard-00-01.o5uq1c1.mongodb.net:27017,ac-wy0xado-shard-00-02.o5uq1c1.mongodb.net:27017/?ssl=true&replicaSet=atlas-11066h-shard-0&authSource=admin&retryWrites=true&w=majority')
db = cluster["sukakita"]

try:
    cluster.admin.command('ping')
    print("You successfully connected to MongoDB!")
except Exception as e:
    print(e)
