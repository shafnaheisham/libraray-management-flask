from flask import Flask, render_template, make_response, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, date
from models import Book, db, User, IssueBook, StudentRegistration
from werkzeug.security import check_password_hash


# Login Resource
class LoginResource(Resource):
    def get(self):
        # Render login page
        response = make_response(render_template("login.html"))
        response.headers["Content-Type"] = "text/html"
        return response

    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity={"id": user.id, "username": user.username})
            return make_response(
                render_template("issue-books.html", message="Login successful", access_token=access_token),
                200,
            )

        return make_response(render_template("login.html", message="Invalid username or password"), 401)


# Book Resource with JWT and Pagination
class BookListResource(Resource):
   
    def get(self):
        
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        books_paginated = Book.query.paginate(page=page, per_page=per_page, error_out=False)
        books = [book.to_dict() for book in books_paginated.items]

        return make_response(
            render_template("add-books.html", books=books, page=page, total_pages=books_paginated.pages), 200
        )

   
    def post(self):
        
        book_data = request.form.to_dict()
        book_data["published_year"] = int(book_data["published_year"])
        book_data["available_copies"] = int(book_data.get("available_copies", 1))

        new_book = Book(**book_data)
        db.session.add(new_book)
        db.session.commit()

        return make_response(render_template("add-books.html", message="New book added successfully"), 201)

    
    def delete(self, book_id):
        
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return make_response(render_template("add-books.html", message="Book deleted"), 200)



class IssueBookResource(Resource):
    
    def get(self, book_id=None):
       
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if book_id:
            issue = IssueBook.query.get(book_id)
            if not issue:
                return make_response(render_template("issue-books.html", message="Issue not found"), 404)
            return make_response(render_template("issue-books.html", issued_books=[issue.to_dict()]), 200)

        issues_paginated = IssueBook.query.paginate(page=page, per_page=per_page, error_out=False)
        issued_books = [issue.to_dict() for issue in issues_paginated.items]

        return make_response(
            render_template("issue-books.html", issued_books=issued_books, page=page, total_pages=issues_paginated.pages),
            200,)

    
    def post(self):
       
        issue_data = request.form.to_dict()

        borrow_date = datetime.strptime(issue_data["borrow_date"], "%Y-%m-%d").date()
        returned_date = datetime.strptime(issue_data["returned_date"], "%Y-%m-%d").date() if issue_data.get("returned_date") else None

        new_issue = IssueBook(
            stud_id=issue_data["stud_id"],
            book_id=issue_data["book_id"],
            borrow_date=borrow_date,
            returned_date=returned_date,
            status=issue_data["status"],
        )

        db.session.add(new_issue)
        db.session.commit()

        return make_response(render_template("issue-books.html", message="Book issued successfully"), 201)

   
    def put(self):
        issue_data = request.form.to_dict()
        book_id=issue_data['book_id'] 
        issue = IssueBook.query.filter_by(book_id=book_id)
        if not issue:
            return make_response(render_template("issue-books.html", message="Issue not found"), 404)

        
        if issue_data.get("returned_date"):
            issue.returned_date = datetime.strptime(issue_data["returned_date"], "%Y-%m-%d").date()
        if issue_data.get("status"):
            issue.status = issue_data["status"]

        db.session.commit()
        return make_response(render_template("issue-books.html", message="Issue updated successfully"), 200)



class StudentResource(Resource):
   
    def get(self, student_id=None):
        
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if student_id:
            student = StudentRegistration.query.get(student_id)
            if not student:
                return make_response(render_template("student.html", message="Student not found"), 404)
            return make_response(render_template("student.html", students=[student.to_dict()]), 200)

        students_paginated = StudentRegistration.query.paginate(page=page, per_page=per_page, error_out=False)
        students = [student.to_dict() for student in students_paginated.items]

        return make_response(
            render_template("student.html", students=students, page=page, total_pages=students_paginated.pages), 200
        )

    
    def post(self):
       
        student_data = request.form.to_dict()
        new_student = StudentRegistration(**student_data)

        db.session.add(new_student)
        db.session.commit()

        return make_response(render_template("student.html", message="Student registered successfully"), 201)

    
    def put(self, student_id):
       
        student = StudentRegistration.query.get(student_id)
        if not student:
            return make_response(render_template("student.html", message="Student not found"), 404)

        student_data = request.form.to_dict()
        for key, value in student_data.items():
            setattr(student, key, value)

        db.session.commit()
        return make_response(render_template("student.html", message="Student updated successfully"), 200)

    
    def delete(self, student_id):
        
        student = StudentRegistration.query.get(student_id)
        if not student:
            return make_response(render_template("student.html", message="Student not found"), 404)

        db.session.delete(student)
        db.session.commit()
        return make_response(render_template("student.html", message="Student deleted successfully"), 200)
