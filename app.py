import streamlit as st
import os
import json

# File to store the bookings data
BOOKINGS_FILE = 'bookings.json'

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

# Streamlit session state for login tracking
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Booking form
def booking_form():
    st.title("Booking Form")
    
    name = st.text_input('Name')
    date = st.date_input('Date')
    time = st.time_input('Time')

    if st.button('Book'):
        if name and date and time:
            # Load existing bookings
            bookings = load_bookings()

            # Create a new booking entry
            booking_id = len(bookings) + 1
            bookings[str(booking_id)] = {'name': name, 'date': str(date), 'time': str(time)}

            # Save the updated bookings to the file
            save_bookings(bookings)

            st.success("Booking successful!")
        else:
            st.error("Please fill in all fields.")

# Admin panel
def admin_panel():
    if not st.session_state.logged_in:
        st.warning("You must be logged in to access the admin panel.")
        return

    st.title("Admin Panel")
    
    # Load existing bookings
    bookings = load_bookings()

    # Display bookings
    for booking_id, booking in bookings.items():
        st.write(f"Booking ID: {booking_id}")
        st.write(f"Name: {booking['name']}")
        st.write(f"Date: {booking['date']}")
        st.write(f"Time: {booking['time']}")
        
        if st.button(f"Delete Booking {booking_id}"):
            # Delete the booking
            del bookings[booking_id]
            save_bookings(bookings)
            st.success(f"Booking ID {booking_id} has been deleted.")
            st.experimental_rerun()

        if st.button(f"Edit Booking {booking_id}"):
            edit_booking_form(booking_id, booking)

# Edit booking form
def edit_booking_form(booking_id, booking):
    st.title(f"Edit Booking ID {booking_id}")

    name = st.text_input('Name', booking['name'])
    date = st.date_input('Date', booking['date'])
    time = st.time_input('Time', booking['time'])

    if st.button('Save Changes'):
        bookings = load_bookings()
        bookings[str(booking_id)] = {'name': name, 'date': str(date), 'time': str(time)}
        save_bookings(bookings)
        st.success(f"Booking ID {booking_id} has been updated.")
        st.experimental_rerun()

# Login form
def login_form():
    st.title("Login")
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if password == '123':  # Use your actual password here
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid password.")

# Logout
def logout():
    st.session_state.logged_in = False
    st.success("Logged out successfully.")
    st.experimental_rerun()

# Main entry point
def main():
    menu = ["Home", "Admin Panel", "Login", "Logout"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Home":
        booking_form()
    elif choice == "Admin Panel":
        admin_panel()
    elif choice == "Login":
        login_form()
    elif choice == "Logout":
        logout()

if __name__ == '__main__':
    main()
