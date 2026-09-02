import sys
import csv


def main():
    reader = csv.reader(sys.stdin)

    for row in reader:

        # Check missing row and header
        if not row or row[0] == "EnrollmentID":
            continue

        # Check missing columns
        if len(row) < 9:
            continue

        course_id = row[2].strip()
        midterm = row[5].strip()
        final_score = row[6].strip()
        total_score = row[7].strip()

        # Check missing data
        if not course_id or not midterm or not final_score or not total_score:
            continue

        # Check invalid number
        try:
            float(midterm)
            float(final_score)
            float(total_score)
        except ValueError:
            continue

        # Emit: key = course_id | value = midterm, final, total
        print(f"{course_id}\t{midterm}\t{final_score}\t{total_score}")


if __name__ == "__main__":
    main()