from flask import render_template,request,redirect,flash,url_for
from User import user
from settings import Students,db
from .validate import validationContent,validateMail
import random
import string



@user.route('/')
def home():
    return render_template('home.html')
    

@user.route('/complaint', methods= ['GET','POST'])
def complaint():
    if request.method == 'POST':
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 6))
        data = dict(request.form)
        if validateMail(data['email']):
            data['body'] = validationContent(data['body'])
            submit_data = Students(code=code,fullName=data['name'],email=data['email'],roll=data['roll'],
                        semester=data['semester'],department=data['dept'],year=data['year'],
                        addressTo=data['addressto'],title=data['title'],body=data['body'])
            db.session.add(submit_data)
            db.session.commit()
            flash(code)
            return redirect(url_for('User.home'))
        else:
            flash('Email is not valid.')
            return redirect(url_for('User.complaint'))
    return render_template('complaint.html')

