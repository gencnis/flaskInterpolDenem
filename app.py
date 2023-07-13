# app.py
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import csv
from CleanData import clearData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(100))
    date_of_birth = db.Column(db.String(100))
    entity_id = db.Column(db.String(100))
    nationalities = db.Column(db.String(100))
    name = db.Column(db.String(100))
    image = db.Column(db.String(1000))

    def __repr__(self):
        return f"Person(id={self.id}, forename={self.forename}, date_of_birth={self.date_of_birth}, " \
               f"entity_id={self.entity_id}, nationalities={self.nationalities}, name={self.name}, image={self.image})"


@app.route('/')
def index():
    """Render the index.html template for the home page."""
    return render_template('index.html')


@app.route('/filter', methods=['POST'])
def filter_data():
    """Filter the data based on the provided criteria and return the results."""
    forename = request.form.get('forename')
    date_of_birth = request.form.get('date_of_birth')
    entity_id = request.form.get('entity_id')
    nationalities = request.form.get('nationalities')
    name = request.form.get('name')
    image = request.form.get('image')

    # Filter the data based on the provided criteria
    filtered_data = Person.query
    if forename:
        filtered_data = filtered_data.filter(Person.forename.ilike(f"%{forename}%"))
    if date_of_birth:
        filtered_data = filtered_data.filter(Person.date_of_birth.ilike(f"%{date_of_birth}%"))
    if entity_id:
        filtered_data = filtered_data.filter(Person.entity_id.ilike(f"%{entity_id}%"))
    if nationalities:
        filtered_data = filtered_data.filter(Person.nationalities.ilike(f"%{nationalities}%"))
    if name:
        filtered_data = filtered_data.filter(Person.name.ilike(f"%{name}%"))
    if image:
        filtered_data = filtered_data.filter(Person.image.ilike(f"%{image}%"))

    results = filtered_data.all()

    return render_template('results.html', results=results)


def read_data(file_path):
    """Read data from the CSV file and return a list of dictionaries."""
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


if __name__ == '__main__':
    with app.app_context():
        # Create the database tables if they don't exist
        db.create_all()

        # Read the data from the CSV file
        file_path = 'data.csv'
        data = read_data(file_path)
        clean_data = clearData(data)

        # Store the data into the database
        for item in clean_data.values():
            person = Person(
                forename=item['forename'],
                date_of_birth=item['date_of_birth'],
                entity_id=item['entity_id'],
                nationalities=item['nationalities'],
                name=item['name'],
                image=item['image']
            )
            db.session.add(person)
        db.session.commit()

        # Run the Flask application in debug mode
        app.run(debug=True)
