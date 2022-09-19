from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "user.db"

def go_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "7lB%ukTU5W!#7TfjIMz!MbUjMPS61%e1W"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .view import view
    from .auth import auth

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models.user import User

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def get_user(uid):
        return User.query.get(str(uid))

    with app.app_context():
        if not User.query.filter(User.user_id == 'mctestface').first():
            user = User(
                user_id = "mctestface",
                pwd = "sha256$FBSLtR1LhzgIHur2$da1e1b0b9669b70c31f7ecfc2e8aefebbd279f9a895549324138179e295a2228",
                ehyp_token = "123",
                qp_id = "123",
                qp_sec = "456",
                con_id_qp = "789",
                bfx_id = "123",
                bfx_sec = "456",
                con_id_bfx = "789",
                region = "Testingen"
            )
            db.session.add(user)
            db.session.commit()

    with app.app_context():
        if not User.query.filter(User.user_id== 'admin').first():
            user = User(
                user_id = "admin",
                pwd = "sha256$Sz9Wu8o7Ge4tRHJC$30ae8e1a88f1135961f114c72eae375110b99e56931e5c8f18635ba86b794a3a",
                ehyp_token = "None",
                qp_id = "None",
                qp_sec = "None",
                con_id_qp = "None",
                bfx_id = "None",
                bfx_sec = "None",
                con_id_bfx = "None",
                region = "Adminhausen"
            )
            db.session.add(user)
            db.session.commit()

    return app

def create_db(app):
    if not path.exists(f"/app/{DB_NAME}"):
        db.create_all(app=app)
        print("Created database successfully!")
    else:
        print("Database was found and connected to the application!")