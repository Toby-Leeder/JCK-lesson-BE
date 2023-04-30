from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.model import Images, getImage # class from model

image_bp = Blueprint("images", __name__, url_prefix='/api/image')
image_api = Api(image_bp)


class ImageAPI(Resource):

    def get(self):
        users = Images.query.all()
        output = []
        for user in users:
            output.append(user.read())
        return jsonify(output)
    
    def post(self):
        body = request.get_json(force=True)
        name = body.get("name")
        data = body.get("data")

        if(not name):
            return "No Name Found"
        if(not data):
            return "No Data Found"
        
        user = Images(name=name, data=data)

        if(user.create() != None):
            return user.read()
        
        return "User creation error, probably a duplicate"
    
    def put(self):
        body = request.get_json(force=True)
        name = body.get("name")
        data = body.get("data")

        if(not name):
            return "No Name Found"
        if(not data):
            return "No Data Found"
        
        try:
            user = getImage(name)
        except:
            return "No User Found"

        if(data):
            try:
                user.update(data=data)
                return f"User with name {user.name} updated with data {data}"
            except:
                return "Update error"
        
        return "Some weird error"
    
    def delete(self):
        body = request.get_json(force=True)
        name = body.get("name")

        if(not name):
            return "No Name Found"
        
        try:
            user = getImage(name)
        except:
            return "No User Found"
        
        user.delete()

        return f"User with name {name} deleted"

        
# make sure to have all of CRUD made here
# make a second api for images as well, in a different file
        

# edit the links below in order to 

image_api.add_resource(ImageAPI, "/")
