from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from sqlalchemy.exc import IntegrityError
from models import SessionLocal, User
from forms import RegistrationForm, LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        db = SessionLocal()
        if db.query(User).filter_by(username=username).first():
            flash("El usuario ya existe", "error")
            return render_template("register.html", form=form)

        user = User(
            username=username,
            password_hash=generate_password_hash(password), # Aquí se cifra
            is_admin=(username == "admin")
        )
        db.add(user)
        db.commit()
        db.close() # Cierra la sesión de DB

        flash("Usuario creado correctamente", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        db = SessionLocal()
        user = db.query(User).filter_by(username=username).first()
        db.close()

        # Comparamos la contraseña en plano contra el hash de la DB
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Credenciales incorrectas", "error")
    
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
