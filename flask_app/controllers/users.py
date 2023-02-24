from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.user import User

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/signup", methods=['POST'])
def signup():
    print(request.form)
    #Validating out user
    if not User.validate_user_info(request.form):
        print("user invalid")
        # redirect('/signup')
        return redirect('/register')
    #Creating a hash password 
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)
    #Saving user to database
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    #saves users info
    user_id = User.save_user(user_data) 
    
    #Logs in the user
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login_user():
    print(request.form)
    user = User.get_by_email(request.form)
    if not user:
        flash("The user name and password provided do not correspond to any account.", 'email')
        return redirect("/login")
    password_valid = bcrypt.check_password_hash(user.password, request.form['password'])
    print(password_valid)
    if not password_valid:
        flash("The user name and password provided do not correspond to any account.", 'password')
        return redirect("/login")
    
    #Loging user in
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name

    return redirect("/recipes")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
