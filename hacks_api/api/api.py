from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.model import Player, getPlayer, quicksort # class from model

player_bp = Blueprint("leaderboards", __name__, url_prefix='/api/players')
player_api = Api(player_bp)


class PlayerAPI(Resource):

    def get(self):
        users = Player.query.all()
        output = []
        for user in users:
            output.append(user.read())
        return jsonify(output)
    
    def post(self):
        body = request.get_json(force=True)
        name = body.get("name")
        tokens = body.get("tokens")

        if(not name):
            return "No Name Found"
        
        user = Player(name=name)

        if(tokens):
            user.tokens = tokens
            
        if(user.create() != None):
            return user.read()
        
        return "User creation error, probably a duplicate"
    
    def put(self):
        body = request.get_json(force=True)
        name = body.get("name")
        tokens = body.get("tokens")

        if(not name):
            return "No Name Found"
        
        try:
            user = getPlayer(name)
        except:
            return "No User Found"

        if(tokens):
            try:
                user.update(tokens=tokens)
                return f"User with name {user.name} updated with tokens {tokens}"
            except:
                return "Update error"
        
        return "Some weird error"
    
    def delete(self):
        body = request.get_json(force=True)
        name = body.get("name")

        if(not name):
            return "No Name Found"
        
        try:
            user = getPlayer(name)
        except:
            return "No User Found"
        
        user.delete()

        return f"User with name {name} deleted"

        
# make sure to have all of CRUD made here
# make a second api for images as well, in a different file

class SortedPlayerAPI(Resource):
    def get(self):
        players = Player.query.all()
        tokens = []
        for player in players:
            tokens.append(player.tokens)
        sortedArray = quicksort(tokens)
        arrays = []
        for i, p in enumerate(players):
            player = Player.query.filter_by(_tokens=sortedArray[i]).first()
            arrays.append([player.name, player.tokens])
        return arrays

        

# edit the links below in order to 

player_api.add_resource(PlayerAPI, "/")
player_api.add_resource(SortedPlayerAPI, "/sort")