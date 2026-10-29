
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

        # Check whether the student exists.
        cursor.execute(
            "SELECT student_id FROM students WHERE student_id = %s",
            (student_id,)
        )

        if cursor.fetchone() is None:
            return jsonify({
                "success": False,
                "error": "Student not found."
            }), 404

        # Remove this student's placement record.
        cursor.execute(
            "DELETE FROM placements WHERE student_id = %s",
            (student_id,)
        )

        # Remove this student's skill links.
        cursor.execute(
            "DELETE FROM student_skills WHERE student_id = %s",
            (student_id,)
        )

        # Delete the student.
        cursor.execute(
            "DELETE FROM students WHERE student_id = %s",
            (student_id,)
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Student and linked records deleted successfully."
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


# GET: Retrieve available skills for student forms
@app.route("/api/available-skills", methods=["GET"])
def get_available_skills():
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
            SELECT skill_id, skill_name
            FROM skills
            ORDER BY skill_name
        """)

        skills = cursor.fetchall()

        return jsonify({
            "success": True,
            "data": skills
        }), 200

    except mysql.connector.Error:
        app.logger.exception("Unable to retrieve available skills")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve available skills."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()



@app.route("/api/students/<int:student_id>/skills", methods=["GET"])
def get_student_skills(student_id):
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
            SELECT skill_id, skill_name
            FROM skills
            WHERE skill_id IN (
                SELECT skill_id
                FROM student_skills
                WHERE student_id = %s
            )
            ORDER BY skill_name
        """, (student_id,))

        skills = cursor.fetchall()

        return jsonify({
            "success": True,
            "data": skills
        }), 200

    except mysql.connector.Error:
        app.logger.exception("Unable to retrieve student skills")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve student skills."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()



# POST: Add skills to an existing student
@app.route("/api/students/<int:student_id>/skills", methods=["POST"])
def add_student_skills(student_id):
    connection = None
    cursor = None

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Please send skill details as JSON."
        }), 400

    skill_ids = data.get("skill_ids")

    if not isinstance(skill_ids, list):
        return jsonify({
            "success": False,
            "error": "skill_ids must be a list."
        }), 400

    if any(
        isinstance(skill_id, bool) or not isinstance(skill_id, int)
        for skill_id in skill_ids
    ):
        return jsonify({
            "success": False,
            "error": "Every skill ID must be a whole number."
        }), 400

    # Remove duplicate IDs while preserving their order.
    skill_ids = list(dict.fromkeys(skill_ids))

    try:
        connection = get_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "error": "Unable to connect to the database."
            }), 500

        cursor = connection.cursor(dictionary=True)

        # Check whether the student exists.
        cursor.execute(
            "SELECT student_id FROM students WHERE student_id = %s",
            (student_id,)
        )

        if cursor.fetchone() is None:
            return jsonify({
                "success": False,
                "error": "Student not found."
            }), 404

        # Check that all supplied skill IDs exist.
        if skill_ids:
            placeholders = ", ".join(["%s"] * len(skill_ids))

            cursor.execute(
                f"SELECT skill_id FROM skills "
                f"WHERE skill_id IN ({placeholders})",
                tuple(skill_ids)
            )

            existing_ids = {
                row["skill_id"] for row in cursor.fetchall()
            }

            if existing_ids != set(skill_ids):
                return jsonify({
                    "success": False,
                    "error": "One or more skill IDs do not exist."
                }), 400

            # Remove previously saved skills for this student.
        cursor.execute(
            "DELETE FROM student_skills WHERE student_id = %s",
            (student_id,)
        )

        # Save the currently selected skills.
        if skill_ids:
            cursor.executemany("""
                INSERT INTO student_skills (student_id, skill_id)
                VALUES (%s, %s)
            """, [
                (student_id, skill_id)
                for skill_id in skill_ids
            ])

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Student skills saved successfully."
        }), 200

    except mysql.connector.Error:
        if connection:
            connection.rollback()

        app.logger.exception("Unable to save student skills")

        return jsonify({
            "success": False,
            "error": "Unable to save student skills."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# GET: Retrieve saved placement details
@app.route("/api/students/<int:student_id>/placement", methods=["GET"])
def get_student_placement(student_id):
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
            SELECT company, job_role, package_lpa,
                   placement_date, status
            FROM placements
            WHERE student_id = %s
        """, (student_id,))

        placement = cursor.fetchone()

        if placement is None:
            return jsonify({
                "success": True,
                "data": None
            }), 200

        if placement["package_lpa"] is not None:
            placement["package_lpa"] = float(
                placement["package_lpa"]
            )

        if placement["placement_date"] is not None:
            placement["placement_date"] = (
                placement["placement_date"].isoformat()
            )

        return jsonify({
            "success": True,
            "data": placement
        }), 200

    except mysql.connector.Error:
        app.logger.exception("Unable to retrieve placement details")
        return jsonify({
            "success": False,
            "error": "Unable to retrieve placement details."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# POST: Add placement details to an existing student
@app.route("/api/students/<int:student_id>/placement", methods=["POST"])
def add_student_placement(student_id):
    connection = None
    cursor = None

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Please send placement details as JSON."
        }), 400

    company = data.get("company")
    job_role = data.get("job_role")
    package_lpa = data.get("package_lpa")
    placement_date = data.get("placement_date")
    status = data.get("status")

    if not isinstance(company, str) or not company.strip():
        return jsonify({
            "success": False,
            "error": "Company name is required."
        }), 400

    if not isinstance(job_role, str) or not job_role.strip():
        return jsonify({
            "success": False,
            "error": "Job role is required."
        }), 400

    if not isinstance(status, str) or not status.strip():
        return jsonify({
            "success": False,
            "error": "Placement status is required."
        }), 400

    company = company.strip()
    job_role = job_role.strip()
    status = status.strip()

    if len(company) > 100 or len(job_role) > 100 or len(status) > 20:
        return jsonify({
            "success": False,
            "error": "One or more placement fields exceed the allowed length."
        }), 400

    # Package and date are optional.
    if package_lpa == "":
        package_lpa = None

    if placement_date == "":
        placement_date = None

    if package_lpa is not None:
        try:
            package_lpa = float(package_lpa)

            if package_lpa < 0:
                raise ValueError

        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "Package must be a valid non-negative number."
            }), 400

    if placement_date is not None:
        from datetime import date

        try:
            date.fromisoformat(placement_date)
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "Placement date must use YYYY-MM-DD format."
            }), 400

    try:
        connection = get_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "error": "Unable to connect to the database."
            }), 500

        cursor = connection.cursor()

        # Check that the student exists.
        cursor.execute(
            "SELECT student_id FROM students WHERE student_id = %s",
            (student_id,)
        )

        if cursor.fetchone() is None:
            return jsonify({
                "success": False,
                "error": "Student not found."
            }), 404

        # Allow only one placement record per student.
        cursor.execute(
            "SELECT placement_id FROM placements WHERE student_id = %s",
            (student_id,)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                "success": False,
                "error": "This student already has a placement record."
            }), 409

        cursor.execute("""
            INSERT INTO placements
                (student_id, company, job_role, package_lpa,
                 placement_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            student_id,
            company,
            job_role,
            package_lpa,
            placement_date,
            status
        ))

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Placement details saved successfully."
        }), 201

    except mysql.connector.Error:
        if connection:
            connection.rollback()

        app.logger.exception("Unable to save student placement")

        return jsonify({
            "success": False,
            "error": "Unable to save placement details."
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
