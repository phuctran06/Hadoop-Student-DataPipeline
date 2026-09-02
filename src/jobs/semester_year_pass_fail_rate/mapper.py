import sys
import csv


def is_pass(letter_grade):
    return "Pass" if letter_grade != "F" else "Fail"


def main():

    reader = csv.reader(sys.stdin)

    for row in reader:

        # Check missing row and header
        if not row or row[0] == "EnrollmentID":
            continue

        # Check missing columns
        if len(row) < 9:
            continue

        semester = row[3].strip()
        year = row[4].strip()
        letter_grade = row[8].strip()

        # Check missing data
        if not semester or not year or not letter_grade:
            continue

        result = is_pass(letter_grade)

        # Emit: key = semester + year | value = Pass/Fail
        print(f"{semester}\t{year}\t{result}")


if __name__ == "__main__":
    main()