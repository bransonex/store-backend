import pymongo
import json
from bson import ObjectId

# connection string

# get the specific database from the db service






# create a class that knows how to parse Object Id into json string
#because json.dumps can not handle ObjectId returned by the db
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)

        return json.JSONEncoder.default(obj)



def json_parse(data):
    return JSONEncoder().encode(data)