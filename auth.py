from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Room, Bet, db
from flask_socketio import join_room, leave_room, send

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your email and password.')
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth.route('/create_room', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        category = request.form.get('category')
        new_room = Room(category=category, owner_id=current_user.id)
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('room', room_id=new_room.id))
    return render_template('create_room.html')

@auth.route('/room/<int:room_id>', methods=['GET', 'POST'])
@login_required
def room(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        bet_amount = request.form.get('bet_amount')
        new_bet = Bet(amount=bet_amount, user_id=current_user.id, room_id=room_id)
        db.session.add(new_bet)
        db.session.commit()
    bets = Bet.query.filter_by(room_id=room_id).all()
    return render_template('room.html', room=room, bets=bets)

@auth.route('/leaderboard/<int:room_id>')
@login_required
def leaderboard(room_id):
    room = Room.query.get_or_404(room_id)
    bets = Bet.query.filter_by(room_id=room_id).all()
    leaderboard = {}
    for bet in bets:
        if bet.user_id not in leaderboard:
            leaderboard[bet.user_id] = 0
        leaderboard[bet.user_id] += bet.amount
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    return render_template('leaderboard.html', room=room, leaderboard=sorted_leaderboard)

@auth.route('/chat/<int:room_id>')
@login_required
def chat(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('chat.html', room=room)

@auth.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    send(f"{data['username']} has joined the room.", to=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    send(f"{data['username']} has left the room.", to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    send(f"{data['username']}: {data['message']}", to=room)

@socketio.on('send_notification')
def handle_send_notification(data):
    send(data['message'], to=data['room'])
