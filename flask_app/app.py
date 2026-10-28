
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
import mysql.connector

from analysis.database import get_connection
from analysis.skills_analysis import analyze_skills
from analysis.package_analysis import analyze_packages
from analysis.company_analysis import analyze_companies
from analysis.department_analysis import analyze_departments


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8000"}})


# --------------------------------------------------
# HOME AND TEST ROUTES
# --------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Student Placement Data Analysis System API",
        "status": "running"
    })


@app.route("/api/test")
def test_api():
    return jsonify({
        "success": True,
        "message": "Flask API is working!"
    })


# --------------------------------------------------
# EXISTING ANALYSIS APIs
# --------------------------------------------------

@app.route("/api/departments")
def department_data():
    try:
        df = analyze_departments()

        if df is None or df.empty:
            return jsonify({"success": True, "data": []})

        return jsonify({
            "success": True,
            "data": df.to_dict(orient="records")
        })

    except Exception:
        app.logger.exception("Department analysis failed")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve department data."
        }), 500


@app.route("/api/companies")
def company_data():
    try:
        df = analyze_companies()

        if df is None or df.empty:
            return jsonify({"success": True, "data": []})

        return jsonify({
            "success": True,
            "data": df.to_dict(orient="records")
        })

    except Exception:
        app.logger.exception("Company analysis failed")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve company data."
        }), 500


@app.route("/api/packages")
def package_data():
    try:
        df = analyze_packages()

        if df is None or df.empty:
            return jsonify({"success": True, "data": []})

        return jsonify({
            "success": True,
            "data": df.to_dict(orient="records")
        })

    except Exception:
        app.logger.exception("Package analysis failed")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve package data."
        }), 500


@app.route("/api/skills")
def skills_data():
    try:
        df = analyze_skills()

        if df is None or df.empty:
            return jsonify({"success": True, "data": []})

        return jsonify({
            "success": True,
            "data": df.to_dict(orient="records")
        })

    except Exception:
        app.logger.exception("Skills analysis failed")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve skills data."
        }), 500


# --------------------------------------------------
# STUDENT CRUD APIs
# --------------------------------------------------

# READ: Get all students
@app.route("/api/students", methods=["GET"])
def get_students():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "error": "Unable to connect to the database."
            }), 500

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT student_id, roll_no, department, graduation_year
            FROM students
            ORDER BY student_id
        """)

        students = cursor.fetchall()

        return jsonify({
            "success": True,
            "data": students
        }), 200

    except mysql.connector.Error:
        app.logger.exception("Unable to retrieve students")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve students."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# READ: Get one student
@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "error": "Unable to connect to the database."
            }), 500

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT student_id, roll_no, department, graduation_year
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        student = cursor.fetchone()

        if student is None:
            return jsonify({
                "success": False,
                "error": "Student not found."
            }), 404

        return jsonify({
            "success": True,
            "data": student
        }), 200

    except mysql.connector.Error:
        app.logger.exception("Unable to retrieve student")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve student."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# CREATE: Add a student
@app.route("/api/students", methods=["POST"])
def create_student():
    connection = None
    cursor = None

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Please send student details as JSON."
        }), 400

    roll_no = data.get("roll_no")
    department = data.get("department")
    graduation_year = data.get("graduation_year")

    if not all([
        isinstance(roll_no, str) and roll_no.strip(),
        isinstance(department, str) and department.strip(),
        graduation_year is not None
    ]):
        return jsonify({
            "success": False,
            "error": "Roll number, department, and graduation year are required."
        }), 400

    roll_no = roll_no.strip()
    department = department.strip()

    if len(roll_no) > 20:
        return jsonify({
            "success": False,
            "error": "Roll number must not exceed 20 characters."
        }), 400

    if len(department) > 50:
        return jsonify({
            "success": False,
            "error": "Department must not exceed 50 characters."
        }), 400

    if isinstance(graduation_year, bool) or not isinstance(graduation_year, int):
        return jsonify({
            "success": False,
            "error": "Graduation year must be a whole number."
        }), 400

    if not 1900 <= graduation_year <= 2100:
        return jsonify({
            "success": False,
            "error": "Please enter a valid graduation year."
        }), 400

    try:
        connection = get_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "error": "Unable to connect to the database."
            }), 500

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students (roll_no, department, graduation_year)
            VALUES (%s, %s, %s)
        """, (roll_no, department, graduation_year))

        new_student_id = cursor.lastrowid
        connection.commit()

        return jsonify({
            "success": True,
            "message": "Student added successfully.",
            "student_id": new_student_id
        }), 201

    except mysql.connector.IntegrityError:
        if connection:
            connection.rollback()

        return jsonify({
            "success": False,
            "error": "This roll number already exists."
        }), 409

    except mysql.connector.Error:
        if connection:
            connection.rollback()

        app.logger.exception("Unable to create student")
        return jsonify({
            "success": False,
            "error": "Unable to add student."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# UPDATE: Edit a student
@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    connection = None
    cursor = None

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Please send updated student details as JSON."
        }), 400

    roll_no = data.get("roll_no")
    department = data.get("department")
    graduation_year = data.get("graduation_year")

    if not all([
        isinstance(roll_no, str) and roll_no.strip(),
        isinstance(department, str) and department.strip(),
        graduation_year is not None
    ]):
        return jsonify({
            "success": False,
            "error": "Roll number, department, and graduation year are required."
        }), 400

    roll_no = roll_no.strip()
    department = department.strip()

    if len(roll_no) > 20 or len(department) > 50:
        return jsonify({
            "success": False,
            "error": "Roll number or department exceeds the allowed length."
        }), 400

    if isinstance(graduation_year, bool) or not isinstance(graduation_year, int):
        return jsonify({
            "success": False,
            "error": "Graduation year must be a whole number."
        }), 400

    if not 1900 <= graduation_year <= 2100:
        return jsonify({
            "success": False,
            "error": "Please enter a valid graduation year."
        }), 400

    try:
        connection = get_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "error": "Unable to connect to the database."
            }), 500

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE students
            SET roll_no = %s,
                department = %s,
                graduation_year = %s
            WHERE student_id = %s
        """, (roll_no, department, graduation_year, student_id))

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT student_id FROM students WHERE student_id = %s",
                (student_id,)
            )

            if cursor.fetchone() is None:
                return jsonify({
                    "success": False,
                    "error": "Student not found."
                }), 404

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Student updated successfully."
        }), 200

    except mysql.connector.IntegrityError:
        if connection:
            connection.rollback()

        return jsonify({
            "success": False,
            "error": "That roll number is already assigned to another student."
        }), 409

    except mysql.connector.Error:
        if connection:
            connection.rollback()

        app.logger.exception("Unable to update student")
        return jsonify({
            "success": False,
            "error": "Unable to update student."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# DELETE: Delete a student only when no related records exist
@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "error": "Unable to connect to the database."
            }), 500

        cursor = connection.cursor()

        cursor.execute(
            "SELECT student_id FROM students WHERE student_id = %s",
            (student_id,)
        )

        if cursor.fetchone() is None:
            return jsonify({
                "success": False,
                "error": "Student not found."
            }), 404

        # Check placement records before attempting deletion.
        cursor.execute(
            "SELECT COUNT(*) FROM placements WHERE student_id = %s",
            (student_id,)
        )
        placement_count = cursor.fetchone()[0]

        # Check skill records before attempting deletion.
        cursor.execute(
            "SELECT COUNT(*) FROM student_skills WHERE student_id = %s",
            (student_id,)
        )
        skill_count = cursor.fetchone()[0]

        if placement_count > 0 or skill_count > 0:
            return jsonify({
                "success": False,
                "error": (
                    "This student has linked placement or skill records. "
                    "Remove or reassign those records first."
                )
            }), 409

        cursor.execute(
            "DELETE FROM students WHERE student_id = %s",
            (student_id,)
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Student deleted successfully."
        }), 200

    except mysql.connector.Error:
        if connection:
            connection.rollback()

        app.logger.exception("Unable to delete student")
        return jsonify({
            "success": False,
            "error": "Unable to delete student."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------
# CHART IMAGE ROUTE
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHART_DIR = PROJECT_ROOT / "visualization" / "charts"


@app.route("/charts/<path:filename>")
def serve_chart(filename):
    return send_from_directory(CHART_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
