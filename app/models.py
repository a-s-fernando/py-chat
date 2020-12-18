from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #each task will have be uniquely identifiable via this id
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderid = db.Column(db.Integer)
    recipientid = db.Column(db.Integer)
    groupid = db.Column(db.Integer)
    username = db.Column(db.String(20))
    message = db.Column(db.String(200))

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    friendid = db.Column(db.Integer)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requesterid = db.Column(db.Integer)
    requestedid = db.Column(db.Integer)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(30))

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
