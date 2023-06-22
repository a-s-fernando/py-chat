from flask import render_template, redirect, flash
from flask_login import login_required, current_user, logout_user, login_user
from app import app, db, models
from .models import db, User, Message, Friend, Request, Group, Member
from .forms import userForm, messageForm, requestForm


@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_anonymous == True:
        app.logger.info('anonymous index route request')
        flash('You are not logged in.')
        return redirect('/login')
    else:
        app.logger.info('index route request from '+current_user.username)
        form = userForm()
        if form.validate_on_submit():
            if form.username.data != form.password.data:
                flash('Passwords did not match')
                app.logger.warning(current_user.username +
                                   ' failed to change their password')
                return redirect('/')
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password changed!')
            app.logger.info(current_user.username+' changed their password')
            return redirect('/login')
        return render_template('home.html', title='WagWapp', username=current_user.username, form=form)


@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    form = requestForm()
    friendlist = current_user.friends
    if form.validate_on_submit():
        userlist = models.User.query.all()
        myid = -1
        for this in userlist:
            if form.user.data == this.username:
                myid = this.id
                break
        if myid == -1:
            flash("user not found")
            return redirect('/friends')
        requestlist = models.Request.query.filter_by(
            requesterid=current_user.id).all()
        for request in requestlist:
            if request.requestedid == myid:
                flash('You already requested them, wait for them to accept')
                return redirect('/friends')
        for friend in friendlist:
            if friend.friendid == myid:
                flash('You are already friends')
                return redirect('/friends')

        newRequest = Request(
            requesterid=current_user.id,
            username=current_user.username,
            requestedid=myid)
        db.session.add(newRequest)
        db.session.commit()
        flash('Request Successful')
        return redirect('/friends')
    return render_template('display.html', title='Friends', list=friendlist, group=False, purpose='Add a new friend:', inputlabel='Their username', form=form)


@app.route('/friends/<number>/thischat', methods=['GET', 'POST'])
@login_required
def friendchat(number):  # number is just the id of the friend
    messagelist = models.Message.query.all()
    filteredlist = []
    for message in messagelist:
        if message.senderid == current_user.id:
            if message.recipientid == int(number):
                filteredlist.append(message)
        if message.recipientid == current_user.id:
            if message.senderid == int(number):
                filteredlist.append(message)
    return render_template('messenger.html', messages=filteredlist, id=int(number), nonav=True)


@app.route('/friends/<number>', methods=['GET', 'POST'])
@login_required
def friendchatsend(number):  # number is just the id of the friend
    form = messageForm()
    them = models.User.query.filter_by(id=int(number)).first()
    theirname = them.username
    if form.validate_on_submit():
        newMessage = Message(
            groupid=0,
            senderid=current_user.id,
            recipientid=int(number),
            username=current_user.username,
            message=form.message.data)
        db.session.add(newMessage)
        db.session.commit()
        return redirect('/friends/'+number)
    app.logger.info(current_user.username+' is talking to '+theirname)
    return render_template('messageframe.html', title='Chat with '+theirname, form=form, id=int(number))


@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    form = requestForm()
    if form.validate_on_submit():
        duplicate = models.Group.query.filter_by(
            groupname=form.user.data).first()
        if duplicate:
            flash('Group name taken')
            return redirect('/groups')
        newGroup = Group(
            groupname=form.user.data)
        db.session.add(newGroup)
        db.session.commit()
        flash('Group creation Successful')
        app.logger.info(current_user.username +
                        ' made a new group called '+form.user.data)
        newgroup = models.Group.query.filter_by(
            groupname=form.user.data).first()
        newMember = Member(
            groupid=newgroup.id,
            userid=current_user.id,
            groupname=newgroup.groupname)
        db.session.add(newMember)
        db.session.commit()
        return redirect('/groups')
    grouplist = current_user.groups
    return render_template('display.html', title='Groups', list=grouplist, group=True, purpose='Create a new group:', inputlabel='New group name', form=form)


@app.route('/groups/<number>/thischat', methods=['GET', 'POST'])
@login_required
def groupchat(number):  # number is just the id of the friend
    messagelist = models.Message.query.all()
    filteredlist = []
    for message in messagelist:
        if message.groupid == int(number):
            filteredlist.append(message)
    return render_template('messenger.html', messages=filteredlist, nonav=True, group=True, id=int(number))


@app.route('/groups/<number>', methods=['GET', 'POST'])
@login_required
def groupchatsend(number):  # number is just the id of the friend
    form = messageForm()
    group = models.Group.query.filter_by(id=int(number)).first()
    memberlist = group.members
    joined = False
    for member in memberlist:
        if member.userid == current_user.id:
            joined = True
            break
    if joined == False:
        flash('Not authorised to view group')
        app.logging.warning(current_user.username +
                            ' tried to access '+group.groupname+' unauthorised')
        return redirect('/groups')
    app.logger.info(current_user.username+' is talking to '+group.groupname)
    if form.validate_on_submit():
        newMessage = Message(
            groupid=int(number),
            senderid=current_user.id,
            recipientid=0,
            username=current_user.username,
            message=form.message.data)
        db.session.add(newMessage)
        db.session.commit()
        return redirect('/groups/'+number)
    return render_template('messageframe.html', title='Chat with '+group.groupname, form=form, group=True, id=int(number))


@app.route('/groups/join', methods=['GET', 'POST'])
@login_required
def join():
    form = requestForm()
    if form.validate_on_submit():
        chosengroup = models.Group.query.filter_by(
            groupname=form.user.data).first()
        if chosengroup:
            newMember = Member(
                groupid=chosengroup.id,
                userid=current_user.id,
                groupname=chosengroup.groupname)
            db.session.add(newMember)
            db.session.commit()
            flash('Group successfully joined')
            app.logger.info(current_user.username +
                            ' joined '+chosengroup.groupname)
            return redirect('/groups/join')
        flash('No group of that name')
        return redirect('/groups/join')
    return render_template('display.html', title='Join a Group', join=True, purpose='Enter the name of the group you want to join:', inputlabel='Group name', form=form)


@app.route('/requests', methods=['GET'])
@login_required
def requests():
    requestlist = current_user.requests
    empty = 1
    for request in requestlist:
        empty = 0
        break
    if empty == 0:
        return render_template('requests.html', title='Requests', list=requestlist)
    else:
        return render_template('requests.html', title='Requests')


@app.route('/requests/<number>', methods=['GET', 'POST'])
@login_required
def accept(number):  # number is just the id of the request
    # figure out how to remove a fucker from the db
    yourname = current_user.username
    yourid = current_user.id
    request = models.Request.query.filter_by(id=number).first()
    theirname = request.username
    theirid = request.requesterid
    yourFriend = Friend(
        userid=yourid,
        friendid=theirid,
        username=theirname)
    theirFriend = Friend(
        userid=theirid,
        friendid=yourid,
        username=yourname)
    db.session.add(yourFriend)
    db.session.add(theirFriend)
    db.session.delete(request)
    db.session.commit()
    flash('Friend added')
    app.logger.info(current_user.username +
                    ' accepted a request from '+theirname)
    return redirect('/requests')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = userForm()
    if form.validate_on_submit():
        duplicate = models.User.query.filter_by(
            username=form.username.data).first()
        if duplicate:
            flash('Username taken')
            return redirect('/register')
        newUser = User(
            username=form.username.data,
            password=form.password.data)
        db.session.add(newUser)
        db.session.commit()
        app.logger.info('A new user named '+form.username.data+' joined')
        flash('You registered!')
        return redirect('/login')
    return render_template('user.html', title='register', login=True, purpose='Register below', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = userForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        users = models.User.query.all()
        for this in users:
            if this.username == username and this.password == password:
                login_user(this, remember=True)
                app.logger.info(username+' logged in')
                return redirect('/')
        app.logger.warning('Someone failed to log in as '+username)
        flash('Wrong credentials.')
        return redirect('/login')
    return render_template('user.html', title='login', login=True, purpose='Login below', form=form)


@app.route('/logout')
@login_required
def logout():
    app.logger.info(current_user.username+' logged out')
    logout_user()
    return redirect('/')
