from sqlalchemy import Column, Integer, String, Text
from .. import app, db
from sqlalchemy.exc import IntegrityError
import json

# place your model code here
# you can use the code we showed in our lesson as an example

class Player(db.Model):
    __tablename__ = 'players'

    _name = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    _tokens = db.Column(db.Integer)

    def __init__(self, name, tokens=0):
        self._name = name
        self._tokens = tokens

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def tokens(self):
        return self._tokens
    
    @tokens.setter
    def tokens(self, tokens):
        self._tokens = tokens

    def create(self):
        try:
            db.session.add(self) 
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "name": self.name,
            "tokens": self.tokens,
        }

    def update(self, name="", tokens=0):
        if len(name) > 0:
            self.name = name
        if tokens > 0:
            self.tokens = tokens
        db.session.commit()
        return self

    def delete(self):
        player = self
        db.session.delete(self)
        db.session.commit()
        return player
    
def getPlayer(name):
    return Player.query.filter_by(_name=name).first()

def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    right = [x for x in arr[1:] if x < pivot]
    left = [x for x in arr[1:] if x >= pivot]

    return quicksort(left) + [pivot] + quicksort(right)

def initPlayers():
    with app.app_context():
        try:
            u1 = Player(name="dash", tokens=123)
            u2 = Player(name="toby", tokens=0)
            players = [u1, u2]
            for player in players:
                player.create()
        except:
            print("database user creation error")


# make sure you put initial data here as well
# EXTRA CREDIT: make the placing of data more efficient than our method shown in the lesson