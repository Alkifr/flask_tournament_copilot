from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_socketio import SocketIO, join_room, leave_room, send
from admin import admin
from api import get_fixtures, get_results, get_live_status, get_euro_2024_fixtures, get_champions_league_2024_2025_fixtures

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

admin.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fixtures', methods=['GET'])
def fixtures():
    competition = request.args.get('competition', 'euro_2024')
    if competition == 'champions_league_2024_2025':
        fixtures = get_champions_league_2024_2025_fixtures()
    else:
        fixtures = get_euro_2024_fixtures()
    return render_template('fixtures.html', fixtures=fixtures)

@app.route('/results')
def results():
    league_id = request.args.get('league_id')
    season = request.args.get('season')
    results = get_results(league_id, season)
    return render_template('results.html', results=results)

@app.route('/live')
def live():
    live_status = get_live_status()
    return render_template('live.html', live_status=live_status)

if __name__ == '__main__':
    socketio.run(app, debug=True)
