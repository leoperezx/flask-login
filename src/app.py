from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
# from markupsafe import escape
from config import config
# Models:
from models.ModelUser import ModelUser
# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app) 

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
        
    else: 
        return render_template('auth/login.html')


@app.route('/new_user')
def new_user():
    return render_template('new_user/new_user.html')
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))       

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/mapa')
@login_required
def mapa():
    return "<h1>ESta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada.</h1>",  404

if __name__=='__main__':
    # carga las configuraciones para el servidor y para la base de datos que provienen del archivo "config.py"
    app.config.from_object(config['development']) 
    # adición para la seguridad de la pagina
    csrf.init_app(app)
    # redirección cuando intentan poner la ruta sin estar "logged"
    app.register_error_handler(401,status_401)
    # mensaje de error cuando no existe la ruta (ejecuta la funcion "status_404(error)" )
    app.register_error_handler(404,status_404)
    # lanza o inicia la app
    app.run()
     
