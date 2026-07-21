from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'
app.config['SECRET_KEY'] = 'change-this-later-to-something-random'  # needed for login sessions

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # redirects here if not logged in

# ---- Models ----

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---- Routes ----

@app.route('/')
def home():
    flights = Flight.query.all()
    return render_template('flights.html', flights=flights)

@app.route('/book/<int:flight_id>', methods=['POST'])
@login_required
def book_flight(flight_id):
    new_booking = Booking(user_id=current_user.id, flight_id=flight_id)
    db.session.add(new_booking)
    db.session.commit()
    flash('Flight booked successfully!')
    return redirect(url_for('home'))

@app.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    # For each booking, get the actual flight details
    booked_flights = [Flight.query.get(b.flight_id) for b in bookings]
    return render_template('my_bookings.html', flights=booked_flights)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already taken
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Try logging in.')
            return redirect(url_for('signup'))

        # Hash the password — we NEVER store plain text passwords
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        # check_password_hash compares the entered password against the stored hash
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Flight.query.count() == 0:
            sample_flights = [
                Flight(airline="SriLankan Airlines", origin="Colombo", destination="Dubai", price=350),
                Flight(airline="Emirates", origin="Colombo", destination="London", price=620),
                Flight(airline="Qatar Airways", origin="Colombo", destination="Singapore", price=280),
            ]
            db.session.add_all(sample_flights)
            db.session.commit()

    app.run(debug=True, host='0.0.0.0', port=5000)