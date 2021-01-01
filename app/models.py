from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #each task will have be uniquely identifiable via this id
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    friends = db.relationship('Friend', backref='user', lazy='dynamic')
    requests = db.relationship('Request', backref='user', lazy='dynamic')
    sent = db.relationship('Message', backref='user', lazy='dynamic')
    groups = db.relationship('Member', backref='user', lazy='dynamic')
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderid = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipientid = db.Column(db.Integer)
    groupid = db.Column(db.Integer)
    username = db.Column(db.String(20))
    message = db.Column(db.String(200))

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    friendid = db.Column(db.Integer)
    username = db.Column(db.String(20))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requesterid = db.Column(db.Integer)
    username = db.Column(db.String(20))
    requestedid = db.Column(db.Integer, db.ForeignKey('user.id'))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(30))
    members = db.relationship('Member', backref='group', lazy='dynamic')

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.Integer, db.ForeignKey('group.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    groupname = db.Column(db.String(30))
