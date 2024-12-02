from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json


app = Flask(__name__)

# File to store the bookings data
BOOKINGS_FILE = 'bookings.json'

# Secret key for session
app.secret_key = 'your_secret_key_here'

# Initialize the bookings dictionary if the file doesn't exist
if not os.path.exists(BOOKINGS_FILE):
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump({}, f)

# Load existing bookings from the file
def load_bookings():
    with open(BOOKINGS_FILE, 'r') as f:
        return json.load(f)

# Save bookings to the file
def save_bookings(bookings):
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f, indent=4)

@app.route('/')
def index():
    # Show the booking form
    return render_template('booking_form.html')

@app.route('/book', methods=['POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        
        # Load existing bookings
        bookings = load_bookings()

        # Create a new booking entry
        booking_id = len(bookings) + 1
        bookings[str(booking_id)] = {'name': name, 'date': date, 'time': time}

        # Save the updated bookings to the file
        save_bookings(bookings)

        return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    # Load existing bookings
    bookings = load_bookings()
    return render_template('admin_panel.html', bookings=bookings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == '123':  # Use your actual password here
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return 'Invalid password', 403
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))



@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    # Load bookings as a dictionary
    bookings = load_bookings()

    # Convert booking_id to string to match the keys in the dictionary
    booking_id_str = str(booking_id)

    if booking_id_str in bookings:
        # Delete the booking if it exists
        del bookings[booking_id_str]
        save_bookings(bookings)
        flash(f"Booking ID {booking_id} has been successfully deleted.", "success")
    else:
        flash(f"Booking ID {booking_id} not found.", "error")

    return redirect(url_for('admin'))




@app.route('/edit/<int:booking_id>', methods=['GET', 'POST'])
def edit_booking(booking_id):
    # Load existing bookings
    bookings = load_bookings()
    booking_id = str(booking_id)  # Ensure the key is a string

    if request.method == 'POST':
        # Update booking information
        bookings[booking_id] = {
            'name': request.form['name'],
            'date': request.form['date'],
            'time': request.form['time']
        }

        # Save the updated bookings to the file
        save_bookings(bookings)

        return redirect(url_for('admin'))

    # For GET request, show the form to edit booking
    booking = bookings.get(booking_id)
    if not booking:
        return redirect(url_for('admin'))

    return render_template('edit_booking.html', booking=booking, booking_id=booking_id)


if __name__ == '__main__':
    app.run(debug=True)
