from flask import render_template, redirect
from app import app, db, models
from datetime import date
from .models import db, User, Message, Friend, Request, Group, Member
from .forms import userForm, messageForm, requestForm, groupForm

@app.route('/', methods=['GET'])
def viewtask():
    return render_template('base.html',
                           title='WagWapp')
