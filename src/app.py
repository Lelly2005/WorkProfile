from flask import Flask, render_template, request, jsonify
from os import environ
from dbcontext import db, db_data, db_delete, db_add, health_check
from person import Person
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# הגדרות למסד הנתונים
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI') or 'mysql://flaskapp:password@mysql:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# אתחול SQLAlchemy עם האפליקציה
db.init_app(app)

# יצירת לוגר
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<int:person_id>/", methods=["GET"])
def get_person(person_id):
    logger.info(f"Get request for person {person_id}")
    data = db_data(person_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Person not found"}), 404

@app.route("/", methods=["POST"])
def add_person():
    data = request.get_json()
    logger.info(f"Add person request: {data}")
    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "Missing name or age"}), 400

    new_person = Person(name=data["name"], age=data["age"])
    db_add(new_person)
    return jsonify({"message": "Person added successfully"}), 201

@app.route("/<int:person_id>/", methods=["DELETE"])
def delete_person(person_id):
    logger.info(f"Delete request for person {person_id}")
    if db_delete(person_id):
        return jsonify({"message": "Person deleted successfully"}), 200
    return jsonify({"error": "Person not found"}), 404

@app.route("/health", methods=["GET"])
def health():
    logger.info("Health check requested")
    return jsonify(health_check()), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
