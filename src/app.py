from flask import Flask ,request , jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
app= Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost/pythonMongodb"
mongo= PyMongo(app)

#inicio
@app.route("/users", methods=["POST"])
def create_users():
    username= request.json["username"]    
    password= request.json["password"]    
    email= request.json["email"]
    if username and password and email : 
        hashedPassword= generate_password_hash(password)
        id=mongo.db.users.insert(
            {
                "username": username, 
                "password":hashedPassword,
                "email": email
            }
        )
        response= {
            "id": str(id),
            "username": username, 
            "password":hashedPassword,
            "email": email
        }
        return response
    else: 
        return notFound()

@app.route("/users", methods=["GET"])
def getUsers(): 
    users= mongo.db.users.find()
    response=json_util.dumps(users)
    return Response(response, mimetype="application/json")

@app.route("/users/<id>", methods=["GET"])
def getUser(id):
    user=mongo.db.users.find_one({"_id": ObjectId(id)})
    response= json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route("/users/<id>", methods=["DELETE"])
def deleteUser(id):
    user=mongo.db.users.delete_one({"_id": ObjectId(id)})
    response= jsonify({"message": "User" +  id   + " WAS DELETED SUCCESSFULLY"})
    return response 

@app.route("/users/<id>", methods=["PUT"])
def updateUser(id):     
    username= request.json["username"]    
    password= request.json["password"]
    email= request.json["email"]
    if username and password and email : 
        hashedPassword= generate_password_hash(password)
        mongo.db.users.update_one({"_id": ObjectId(id)}, {"$set": {
            "username": username, 
            "password":hashedPassword,
            "email": email
        }})
        response= jsonify({"message":"User: "+ id + " Was updated succesfully"})
        return response
@app.errorhandler(404)
def notFound(error=None):
    response= jsonify({
        "message":"Resource Not Found: " + request.url ,
        "status": 404
    })
    response.status_code= 404
    return response 
if __name__ == "__main__":
    app.run(debug=True)