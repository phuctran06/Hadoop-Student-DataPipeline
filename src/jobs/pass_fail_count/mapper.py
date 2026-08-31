import sys
import csv

def check_threshold(t):
    return "pass" if t>=5 else "false"


def main():

    reader = csv.reader(sys.stdin)

    for row in reader:
        #Check missing row and firstline
        if row is None or row[0] == "EnrollmentID":
            continue

        #Check missing columns
        if len(row) < 9:
            continue

        if not row[7].strip():
            continue

        #Convert string to float
        try:
            row[7] = float(row[7])
        except ValueError:
            continue

        #Check pass or false
        result = check_threshold(row[7])

        print(f"{result}\t1")

if __name__ == "__main__":
    main()
        
