from flask import Flask, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from models import db, User, Room, Bet

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

# Добавление моделей в административную панель
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Room, db.session))
admin.add_view(AdminModelView(Bet, db.session))

if __name__ == '__main__':
    app.run(debug=True)