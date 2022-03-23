from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User


#TEMPLATE ROUTES
@app.route('/')
def index():
    if "user_id" in session:
        return redirect('/recipes')
    return render_template("index.html")



#ACTION ROUTES
@app.route('/register', methods=['POST'])
def register():
    if User.validate_registry(request.form):
        User.create_user(request.form)
        data = { "email": request.form["email"] }
        user = User.get_user_by_email(data)
        session['user_id'] = user.id
        session['user_first_name'] = request.form["first_name"]
        return redirect('/recipes')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = { "email": request.form["email"] }
    user = User.get_user_by_email(data)
    if not user:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user.id
    session['user_first_name'] = user.first_name
    return redirect('/recipes')