#!/usr/bin/env python3

import sys
import csv


def main():

    reader = csv.reader(sys.stdin)

    for row in reader:
        #Skip header and empty lines
        if not row or row[0] == "EnrollmentID":
            continue

        #Check 
        if len(row) < 2:
            continue

        student_id = row[1].strip()

        if student_id:
            print(f"{student_id}\t1")


if __name__ == "__main__":
    
    main()