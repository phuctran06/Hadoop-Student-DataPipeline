import sys


def main():

    current_course_id = None
    course_name = None
    grade_count = {}

    for line in sys.stdin:

        # Split key and value
        course_id, record_type, value = line.rstrip("\n").split("\t")

        # New CourseID
        if current_course_id is None:
            current_course_id = course_id

        if course_id != current_course_id:

            # Output result
            for grade, count in grade_count.items():
                print(f"{course_name}\t{grade}\t{count}")

            # Reset
            current_course_id = course_id
            course_name = None
            grade_count = {}

        # Get CourseName
        if record_type == "COURSE":
            course_name = value

        # Count LetterGrade
        elif record_type == "ENROLLMENT":

            if value not in grade_count:
                grade_count[value] = 0

            grade_count[value] += 1

    # Output last CourseID
    if current_course_id is not None:

        for grade, count in grade_count.items():
            print(f"{course_name}\t{grade}\t{count}")


if __name__ == "__main__":
    main()