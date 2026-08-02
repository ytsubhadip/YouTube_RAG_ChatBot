from flask import Blueprint, request, jsonify
from database_config import user_collection

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['post'])
def login():
    data= request.get_json()
    print("User data")
    print(data)
    try:
        user_collection.insert_one(data)
        return{"message": "inser user data"}
    except:
         return{"message": "error"}

    return {"message": "databse not connect"}