import csv
import sys


reader = csv.reader(sys.stdin)

for row in reader:

    # Check empty row
    if not row:
        continue

    # Course.csv
    if row[0] == "CourseID":
        continue

    # Enrollment.csv
    if row[0] == "EnrollmentID":
        continue

    # Check Course
    if len(row) == 5:

        course_id = row[0].strip()
        course_name = row[1].strip()

        # Emit Course record
        print(f"{course_id}\tCOURSE\t{course_name}")

    # Check Enrollment
    elif len(row) == 9:

        enrollment_id = row[0].strip()
        course_id = row[2].strip()
        letter_grade = row[8].strip()

        # Check missing data
        if not course_id or not letter_grade:
            continue

        # Emit Enrollment record
        print(f"{course_id}\tENROLLMENT\t{letter_grade}")