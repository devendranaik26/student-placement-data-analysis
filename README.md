
# Student Placement Data Analysis System

## Project Overview

The Student Placement Data Analysis System analyzes student placement outcomes, salary packages, company recruitment, and technical skills using MySQL and Python.

The project uses sample student data for analysis and supports a web dashboard that will be developed by the team.

## Technologies Used

- **MySQL:** Stores student, skill, and placement data.
- **Python:** Implements the analysis logic.
- **Pandas:** Organizes and analyzes tabular data.
- **NumPy:** Performs numerical calculations.
- **Flask:** Web backend (developed by a team member).
- **HTML, CSS, JavaScript:** Frontend (developed by a team member).
- **Matplotlib:** Data visualization (developed by a team member).

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
├── visualization/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Analysis Features

1. Department-wise placement rates.
2. Overall and department-wise salary package statistics.
3. Company-wise placement statistics.
4. Technical skills analysis for placed and unplaced students.

## Database Setup

1. Install MySQL Server and MySQL Workbench.
2. Import the SQL database export from the `sql/` folder, or execute the schema and data scripts in the appropriate order.
3. Configure local database credentials using a `.env` file in the project root.

Example `.env` variable names:

```text
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_local_password
MYSQL_DATABASE=student_placement_db
```

Never commit actual database credentials to GitHub.

## Install Python Dependencies

Install the required libraries:

```bash
pip install pandas numpy mysql-connector-python python-dotenv
```

## Run the Analysis

From the project root, execute:

```bash
python analysis/main.py
```

The program runs the department, package, company, and skills analyses and prints their results in the terminal.

## Team Responsibilities

- **Data analysis:** MySQL, Pandas, NumPy, and analysis modules.
- **Flask backend:** Routes, API endpoints, and integration with analysis functions.
- **Frontend:** HTML, CSS, JavaScript, and dashboard interface.
- **Visualization:** Matplotlib charts for placement and package analysis.

## Data Privacy

Use fictional or approved student data. Do not publish private student information or database passwords.
