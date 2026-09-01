import sys
import csv


STUDENT_PATH = "/app/data/processed/Student.csv"
COURSE_PATH = "/app/data/processed/Course.csv"


def load_students(path):
    students = {}
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] == "StudentID":
                continue
            if len(row) < 6:
                continue
            student_id = row[0].strip()
            first_name = row[1].strip()
            last_name = row[2].strip()
            gender = row[3].strip()
            students[student_id] = (first_name, last_name, gender)
    return students


def load_courses(path):
    courses = {}
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] == "CourseID":
                continue
            if len(row) < 5:
                continue
            course_id = row[0].strip()
            course_name = row[1].strip()
            courses[course_id] = course_name
    return courses


def get_score_range(score):
    if score < 2:
        return "0-2"
    elif score < 4:
        return "2-4"
    elif score < 6:
        return "4-6"
    elif score < 8:
        return "6-8"
    else:
        return "8-10"


def main():

    students = load_students(STUDENT_PATH)
    courses = load_courses(COURSE_PATH)

    reader = csv.reader(sys.stdin)

    for row in reader:

        # Check missing row and header
        if row is None or row[0] == "EnrollmentID":
            continue

        # Check missing columns
        if len(row) < 9:
            continue

        # Check missing TotalScore
        if not row[7].strip():
            continue

        # Convert string to float
        try:
            total_score = float(row[7])
        except ValueError:
            continue

        student_id = row[1].strip()
        course_id = row[2].strip()

        # Lookup student and course info
        student_info = students.get(student_id)
        course_name = courses.get(course_id)

        if student_info is None or course_name is None:
            continue

        first_name, last_name, gender = student_info

        # Get score range
        score_range = get_score_range(total_score)

        # Emit: key = course_name, gender, score_range | value = student full name
        print(f"{course_name}\t{gender}\t{score_range}\t{first_name} {last_name}")


if __name__ == "__main__":
    main()