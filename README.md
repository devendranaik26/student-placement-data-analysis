
# Student Placement Data Analysis System

## Project Overview

The Student Placement Data Analysis System analyzes student placement outcomes, department-wise placement rates, salary packages, company recruitment, and technical skill demand.

The project uses MySQL for data storage, Python for data analysis, Pandas and NumPy for data processing, Flask for the backend APIs, and HTML, CSS, JavaScript, and Chart.js for the interactive web dashboard.

The system provides five dashboard pages with summary cards and charts to help users understand placement trends and compare departments, companies, packages, and technical skills.

## Features

- Department-wise placement rate analysis.
- Comparison of total students and placed students across departments.
- Average, highest, and lowest salary package summaries.
- Package distribution and department-wise package comparison.
- Company-wise placement statistics.
- Technical skill demand analysis.
- Interactive dashboard with five pages and eight charts.
- Flask APIs that provide data to the frontend.
- MySQL database integration.
- Aggregate reporting designed to avoid exposing private student information.

## Technologies Used

- **MySQL:** Stores student, skill, and placement data.
- **Python:** Implements the analysis logic.
- **Pandas:** Processes and analyzes tabular data.
- **NumPy:** Supports numerical calculations.
- **mysql-connector-python:** Connects Python to MySQL.
- **python-dotenv:** Loads local database configuration.
- **Flask:** Provides backend routes and REST API endpoints.
- **HTML:** Structures the dashboard pages.
- **CSS:** Styles the dashboard interface.
- **JavaScript:** Connects the frontend to the backend APIs.
- **Chart.js:** Creates interactive dashboard charts.
- **Matplotlib:** Supports Python-based data visualization where applicable.
- **Git and GitHub:** Support version control and team collaboration.

## Project Structure

```text
student-placement-data-analysis/
├── analysis/
│   ├── __init__.py
│   ├── database.py
│   ├── department_analysis.py
│   ├── package_analysis.py
│   ├── company_analysis.py
│   ├── skills_analysis.py
│   └── main.py
├── python/
│   └── main.py
├── sql/
│   ├── schema.sql
│   ├── analysis.sql
│   └── student_placement_data.sql
├── flask_app/
├── frontend/
│   ├── html/
│   ├── css/
│   └── js/
├── visualization/
├── .gitignore
├── requirements.txt
└── README.md
```

The `.env` file is stored locally and should not be committed to GitHub.

## Database Setup

1. Install MySQL Server and MySQL Workbench.
2. Import `sql/student_placement_data.sql` into MySQL Workbench, or execute the schema and data scripts in the correct order.
3. Confirm that the database `student_placement_db` exists.
4. Create a `.env` file in the project root.
5. Add your local MySQL configuration.

Example `.env` configuration:

```text
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_local_password
MYSQL_DATABASE=student_placement_db
```

Replace the example values with your local MySQL credentials.

**Security:** Never commit your actual `.env` file, database passwords, or private student information to GitHub.

## Install Dependencies

Open a terminal in the project root and run:

```bash
pip install -r requirements.txt
```

Alternatively, install the core analysis dependencies:

```bash
pip install pandas numpy mysql-connector-python python-dotenv
```

Flask and any other dependencies used by the application should also be included in `requirements.txt`.

## Run the Python Analysis

From the project root, run:

```bash
python -m analysis.main
```

This runs the analysis modules for departments, packages, companies, and technical skills, provided the database configuration and required tables are available.

## Run the Flask Backend

Open a terminal in the project root and run:

```bash
python -m flask --app flask_app.app run --debug
```

The Flask server will normally be available at:

```text
http://127.0.0.1:5000
```

Keep this terminal running while using the frontend.

## Run the Frontend

Open a second terminal and run:

```bash
cd frontend
python -m http.server 8000
```

Open the dashboard in your browser:

```text
http://127.0.0.1:8000/html/dashboard.html
```

## Dashboard Pages

| Page | Purpose |
|---|---|
| Dashboard | Overall placement summary and company distribution |
| Department Analysis | Department-wise placement rates and student comparison |
| Package Analysis | Average packages and package distribution |
| Company Analysis | Company-wise placement statistics |
| Skills Analysis | Technical skill demand among students |

The frontend retrieves data from the Flask backend and displays it through interactive charts and summary cards.

## API Endpoints

The Flask backend provides the following endpoints:

| Endpoint | Purpose |
|---|---|
| `/api/departments` | Department-wise placement data |
| `/api/companies` | Company-wise placement statistics |
| `/api/packages` | Salary package records and analysis data |
| `/api/skills` | Technical skill demand data |

Example:

```text
http://127.0.0.1:5000/api/departments
```

The endpoints return JSON responses that the frontend uses to display the dashboard.

## Team Responsibilities

- **Data Analysis:** MySQL, Pandas, NumPy, and analysis modules.
- **Flask Backend:** API routes, database integration, and backend logic.
- **Frontend Development:** HTML, CSS, JavaScript, and dashboard interface.
- **Data Visualization:** Chart.js dashboard charts and Matplotlib visualizations where applicable.

## Data Privacy

- Use fictional or approved student data.
- Prefer aggregate statistics over individual student records.
- Do not publish private student information or database credentials.
- Keep local configuration files and secrets out of version control.

## Future Enhancements

- Add filters for department, company, graduation year, and package range.
- Add more placement and skill-demand insights.
- Improve dashboard responsiveness for mobile devices.
- Add data export options for reports.
- Improve validation and error handling.
