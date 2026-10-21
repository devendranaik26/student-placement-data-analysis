-- Company-wise placement statistics
SELECT
    company,
    COUNT(*) AS total_students,
    ROUND(AVG(package_lpa), 2) AS average_package_lpa,
    MAX(package_lpa) AS highest_package_lpa
FROM placements
GROUP BY company
ORDER BY total_students DESC;


-- Analyze department-wise placement rates
SELECT
    s.department,
    COUNT(s.student_id) AS total_students,
    COUNT(p.placement_id) AS placed_students,
    ROUND(
        COUNT(p.placement_id) * 100.0 /
        COUNT(s.student_id),
        2
    ) AS placement_percentage
FROM students s
LEFT JOIN placements p
    ON s.student_id = p.student_id
GROUP BY s.department
ORDER BY placement_percentage DESC;


-- Analyze salary packages
SELECT
    s.department,
    COUNT(p.placement_id) AS placed_students,
    ROUND(AVG(p.package_lpa), 2) AS average_package_lpa,
    MAX(p.package_lpa) AS highest_package_lpa,
    MIN(p.package_lpa) AS lowest_package_lpa
FROM students s
JOIN placements p
    ON s.student_id = p.student_id
GROUP BY s.department
ORDER BY average_package_lpa DESC;


-- The most common skills among placed students
SELECT
    sk.skill_name,
    COUNT(DISTINCT ss.student_id) AS placed_students_with_skill
FROM student_skills ss
JOIN skills sk
    ON ss.skill_id = sk.skill_id
JOIN placements p
    ON ss.student_id = p.student_id
GROUP BY sk.skill_id, sk.skill_name
ORDER BY placed_students_with_skill DESC;


-- Comparing the skills among placed and unplaced students
SELECT
    sk.skill_name,
    COUNT(DISTINCT CASE
        WHEN p.student_id IS NOT NULL
        THEN s.student_id
    END) AS placed_students,
    COUNT(DISTINCT CASE
        WHEN p.student_id IS NULL
        THEN s.student_id
    END) AS unplaced_students
FROM students s
JOIN student_skills ss
    ON s.student_id = ss.student_id
JOIN skills sk
    ON ss.skill_id = sk.skill_id
LEFT JOIN placements p
    ON s.student_id = p.student_id
GROUP BY sk.skill_id, sk.skill_name
ORDER BY placed_students DESC;