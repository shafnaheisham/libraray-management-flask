from flask import Flask
from flask_restful import Api
from models import db, User, Book
from resources import BookListResource, IssueBookResource, LoginResource, StudentResource
from werkzeug.security import generate_password_hash



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with app
db.init_app(app)



# Initialize API
api = Api(app)

# Routes
api.add_resource(LoginResource, "/login")
api.add_resource(BookListResource, "/books", "/books/<int:book_id>", "/issues/<title>")
api.add_resource(IssueBookResource, "/issues", "/issues/<int:book_id>", "/issues/<int:id>")
api.add_resource(StudentResource, "/student", "/student/<int:stud_id>")

# Function to create tables and default data
def create_tables():
    with app.app_context():
        db.create_all()  # Create tables
        # Add a default user (for testing purposes)
        if not User.query.first():
            default_user = User(username="lib", password=generate_password_hash("123"))
            db.session.add(default_user)
            db.session.commit()

if __name__ == "__main__":
    create_tables()  # Create tables and add default data if necessary
    app.run(debug=True)