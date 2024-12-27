from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_year = db.Column(db.Integer, nullable=False)
    available_copies = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "published_year": self.published_year,
            "available_copies": self.available_copies,
        }




class IssueBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stud_id = db.Column(db.String(120), nullable=False)  # Student ID
    book_id = db.Column(db.Integer, nullable=False)  # Book ID
    borrow_date = db.Column(db.Date, nullable=False, default=date.today)  # Borrow date defaults to today
    returned_date = db.Column(db.Date, nullable=True)  # Can be null if the book is not yet returned
    status = db.Column(db.String(120), nullable=False, default='Not Returned')  # Default status is 'Not Returned'

    def to_dict(self):
        return {
            "id": self.id,
            "stud_id": self.stud_id,
            "book_id": self.book_id,
            "borrow_date": self.borrow_date.isoformat() if self.borrow_date else None,
            "returned_date": self.returned_date.isoformat() if self.returned_date else None,
            "status": self.status
        }
class StudentRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    
    class_name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Active')

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
           
            "class_name": self.class_name,
            "gender": self.gender,
            "status": self.status,
        }