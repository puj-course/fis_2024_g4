from pymongo import MongoClient
client = MongoClient('mongodb+srv://aiurbinamox:123@proyecto.1lqlm.mongodb.net/')
db = client['Proyecto']  
pokemon_collection = db['Pokemon'] 
usuarios_collection = db['Usuarios']
