
import pandas as pd
from database import get_connection


def analyze_skills():
    connection = get_connection()

    if connection is None:
        return None

    try:
        query = """
        SELECT
            sk.skill_name,
            COUNT(DISTINCT ss.student_id) AS total_students_with_skill,
            COUNT(DISTINCT CASE
                WHEN p.student_id IS NOT NULL
                THEN ss.student_id
            END) AS placed_students_with_skill
        FROM skills sk
        JOIN student_skills ss
            ON sk.skill_id = ss.skill_id
        LEFT JOIN placements p
            ON ss.student_id = p.student_id
            AND p.status = 'Placed'
        GROUP BY sk.skill_id, sk.skill_name
        ORDER BY placed_students_with_skill DESC
        """

        skills_df = pd.read_sql(query, connection)

        print("\nSkills Analysis:")
        print(skills_df.to_string(index=False))

        return skills_df

    finally:
        connection.close()
