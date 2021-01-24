from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template,request,redirect,session,url_for
from settings import Students,Admins,db
from .verify import tokenCheck
from Admin import admin
import os


if "SECRET_TOKEN" in os.environ:
    SECRET_TOKEN = os.environ['SECRET_TOKEN']
else:
    SECRET_TOKEN = 'this-is-secret'

@admin.route('/thank-you')
def thankyou():
    if "secret_token" in session:
        session.pop("secret_token", None)
        return render_template('thankyou.html')
    return render_template('thankyou.html')


@admin.route('/add-secret', methods=['GET','POST'])
def secret():
    session.pop("secret_token", None)
    if request.method == "POST":
        secret_token = request.form['secret_token']
        if tokenCheck(secret_token):
            if secret_token == SECRET_TOKEN:
                session["secret_token"] = secret_token
                return redirect(url_for('Admin.register'))
            else:
                return '<h1> Sorry, We can not proceed your request  :( </h1>'
        else:
            return redirect('/admin')
    return render_template('secret.html')


@admin.route('/registration/fg38h43ibcf33owlqpw92gwqe', methods=['GET','POST'])
def register():
    if "secret_token" in session:
        if request.method == "POST":
            adminusername = request.form['adminusername']
            adminemail = request.form['adminemail']
            adminpassword = request.form['adminpassword']
            hash_password = generate_password_hash(adminpassword)
            chk_point = Admins.query.filter_by(adminEmail=adminemail).first()
            if chk_point is None:
                forSubbmit = Admins(adminUser=adminusername,adminEmail=adminemail,adminPassword=hash_password)
                db.session.add(forSubbmit)
                db.session.commit()
                return redirect(url_for('Admin.thankyou'))
            else:
                return '<h1> Sorry ! This User is already exist. Please Use a different Email id :( </h1>'
        return render_template('admin_register.html')
    session.pop("secret_token", None)
    return redirect(url_for('Admin.admin_login'))
    

@admin.route('/login', methods=['GET','POST'])
def admin_login():
    if request.method == "POST":
        useremail = request.form['userEmail']
        password = request.form['password']
        found_user = Admins.query.filter_by(adminEmail=useremail).first_or_404(description='Wrong Input ! Please Enter correct Information')
        cond = check_password_hash(found_user.adminPassword,password)
        if cond:
            session["user"] = useremail
            session["password"] = password
            return redirect(url_for('Admin.dashboard', usr=found_user.adminUser))
        else:
            return redirect(url_for('Admin.admin_login'))
    elif "user" in session:
        found_user = Admins.query.filter_by(adminEmail=session["user"]).first_or_404(description='Wrong Input ! Please Enter correct Information')
        return redirect(url_for('Admin.dashboard', usr=found_user.adminUser))
    return render_template('admin_login.html')


@admin.route('/dashboard/<usr>')
def dashboard(usr):
    if "user" in session:
        complains = Students.query.order_by(Students.date).all()
        complains.reverse()
        return render_template('dashboard.html', user_display=usr, total_compNo=len(complains), all_complains=complains)
    else:
        return redirect(url_for('Admin.admin_login'))


@admin.route('/update/<id>')
def update(id):
    if ("user" in session):
        updt = Students.query.get(id)
        updt.isViewed = 'True'
        db.session.commit()
        found_user = Admins.query.filter_by(adminEmail=session["user"]).first_or_404()
        return redirect(url_for('Admin.dashboard', usr=found_user.adminUser))
    else:
        return redirect('/admin')


@admin.route('/delete/<id>')
def delete(id):
    if "user" in session:
        dlt = Students.query.get(id)
        db.session.delete(dlt)
        db.session.commit()
        found_user = Admins.query.filter_by(adminEmail=session["user"]).first_or_404()
        return redirect(url_for('Admin.dashboard', usr=found_user.adminUser))
    else:
        return redirect('/admin')


@admin.route('/logout')
def logout():
    if "user" in session:
        session.pop("user", None)
        session.pop("password", None)
        return redirect(url_for('Admin.admin_login'))
    return render_template('admin_login.html')
    
