from .extensions import mongo

def insert(item):
    user_collection = mongo.db.users
    usercollection.insert(item)

def find(item):
    user_collection = mongo.db.users
    user =  user_collection.find_one(item)
    if user :
        return user
    return {'error':'no user found'}

def update(item):
    user_collection = mongo.db.users
    user =  user_collection.find_one(item)
    if user : 
        #changes to be made
        user_collection.save(user)
        return user
    return {'error':'no user found'}
    
def delete_item(item):
    user_collection = mongo.db.users
    user =  user_collection.find_one(item)
    if user : 
        user_collection.remove(user)
        return "removed"
    return {'error':'no user found'}