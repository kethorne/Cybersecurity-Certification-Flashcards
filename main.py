# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\ketho\\PycharmProjects\\Cybersecurity Certification Flashcards\\instance\\flashcards.db'

db = SQLAlchemy(app)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', backref=db.backref('flashcards', lazy=True))

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    subjects = Subject.query.all()
    return render_template('home.html', subjects=subjects)

@app.route('/subjects/<int:subject_id>')
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    flashcards = Flashcard.query.filter_by(subject_id=subject_id).all()
    return render_template('subject.html', subject=subject, flashcards=flashcards)

@app.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    question = request.form['question']
    answer = request.form['answer']
    subject_id = request.form['subject_id']
    flashcard = Flashcard(question=question, answer=answer, subject_id=subject_id)
    db.session.add(flashcard)
    db.session.commit()
    return redirect(url_for('index'))

# Route for CompTIA A+ subject page
@app.route('/compTIA_A+')
def comptia_a_plus():
    return render_template('compTIA_A+.html', subject="CompTIA A+")

# Route for CompTIA Network+ subject page
@app.route('/compTIA_Network+')
def comptia_network_plus():
    return render_template('compTIA_Network+.html', subject="CompTIA Network+")

# Route for CompTIA Security+ subject page
@app.route('/compTIA_Security+')
def comptia_security_plus():
    return render_template('compTIA_Security+.html', subject="CompTIA Security+")

if __name__ == '__main__':
    app.run(debug=True)

