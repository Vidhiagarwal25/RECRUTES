import flask
from flask import Flask, render_template, request, jsonify
import pymongo
from pymongo import MongoClient


app = Flask(__name__, static_url_path='/static')

client = MongoClient("mongodb://localhost:27017")
global db
try:
    client.admin.command('ping')
    db = client.placement

    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/jobs')
def jobs():
    sort_operation = ({"Posting_Date": -1})
    limit = 10
    # Execute the query with sort and limit operations
    top_jobs = db.jobs.find().sort(sort_operation).limit(limit)

    # Convert the cursor to a list of dictionaries
    top_jobs_list = list(top_jobs)

    # Pass the top books to the HTML template for rendering
    return render_template('jobs.html', job=top_jobs_list)


@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/asstudent', methods=['GET', 'POST'])
def asstudent():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        gender = request.form['gender']
        address = request.form['address']
        qualification = request.form['qualification']

        # Check if email already exists
        existing_user = db.studentuser.find_one({'email': email})
        if existing_user:
            return render_template('login.html', "Email already exists.", email_exists=True)

        # Insert data into MongoDB collection
        student_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'dob': dob,
            'gender': gender,
            'address': address,
            'qualification': qualification
        }
        db.studentuser.insert_one(student_data)  # Insert data into the collection

        # Redirect to a success page or render another template
        return render_template('home.html', first_name=first_name)
    else:
        return render_template('asstudent.html')

@app.route('/ascompany')
def ascompany():
    return render_template('ascompany.html')


          
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        message = request.form['message']

        # Insert data into MongoDB
        db.message.insert_one({'full_name': full_name, 'email': email, 'message': message})

        return render_template('contact.html', message='Message submitted successfully!')
    else:
        return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
