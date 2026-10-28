from flask import send_from_directory
from pathlib import Path

from analysis.skills_analysis import analyze_skills

from analysis.package_analysis import analyze_packages

from analysis.company_analysis import analyze_companies

from flask import Flask, jsonify

from analysis.department_analysis import analyze_departments

app = Flask(__name__)


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


@app.route("/api/departments")
def department_data():
    try:
        df = analyze_departments()

        if df is None or df.empty:
            return jsonify({
                "success": True,
                "data": []
            })

        # Convert Pandas data into JSON-compatible records
        records = df.to_dict(orient="records")

        return jsonify({
            "success": True,
            "data": records
        })

    except Exception as e:
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
            return jsonify({
                "success": True,
                "data": []
            })

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
            return jsonify({
                "success": True,
                "data": []
            })

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
            return jsonify({
                "success": True,
                "data": []
            })

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


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Folder containing generated chart images
CHART_DIR = PROJECT_ROOT / "visualization" / "charts"


@app.route("/charts/<path:filename>")
def serve_chart(filename):
    return send_from_directory(CHART_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
