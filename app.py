from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session management

# Store the form data in a CSV file
def save_donor_info(name, whatsapp, amount):
    with open('donors.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, whatsapp, amount])

def get_donors():
    donors = []
    if os.path.exists('donors.csv'):
        with open('donors.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                donors.append(row)
    return donors

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/donate', methods=['POST'])
def donate():
    name = request.form['name']
    whatsapp = request.form['whatsapp']
    amount = request.form['amount']
    
    # Validate that the WhatsApp number is exactly 10 digits
    if not (whatsapp.isdigit() and len(whatsapp) == 10):
        return "<h1>Invalid WhatsApp number! Please enter exactly 10 digits.</h1><br><a href='/'>Back to Donation Page</a>"

    # Save donor info if validation passes
    save_donor_info(name, whatsapp, amount)
    
    return redirect(url_for('thank_you'))


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


# Admin login page
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "<h1>Invalid credentials!</h1>"
    return render_template('admin_login.html')

# Admin panel to view donors
@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    donors = get_donors()
    return render_template('admin_panel.html', donors=donors)


@app.route('/clear-data')
def clear_data():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Check if the donors.csv file exists
    if os.path.exists('donors.csv'):
        # Clear the contents of the CSV file
        with open('donors.csv', 'w') as file:
            pass  # Opening in 'w' mode clears the file contents

    return "<h1>All donor data has been cleared!</h1><br><a href='/admin'>Back to Admin Panel</a>"


# Logout for admin
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
