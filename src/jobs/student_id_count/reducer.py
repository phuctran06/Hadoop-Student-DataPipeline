#!/usr/bin/env python3

import sys


def main():

    current_student_id = None
    current_count = 0


    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        try:
            student_id, count = line.split("\t", 1)
            count = int(count)
        except ValueError:
            continue

        if current_student_id == student_id:
            current_count += count

        else:
            # Xuất kết quả của student trước đó
            if current_student_id is not None:
                print(f"{current_student_id}\t{current_count}")

            current_student_id = student_id
            current_count = count

    # Xuất student cuối cùng
    if current_student_id is not None:
        print(f"{current_student_id}\t{current_count}")


if __name__ == "__main__":
    main()