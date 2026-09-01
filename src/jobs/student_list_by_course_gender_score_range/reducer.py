import sys


def main():

    current_key = None
    student_list = []

    for line in sys.stdin:

        # Split key and value
        course_name, gender, score_range, student_name = line.rstrip("\n").split("\t")

        key = (course_name, gender, score_range)

        # Check new group
        if current_key is None:
            current_key = key

        if key != current_key:

            # Output result
            students_str = ", ".join(student_list)
            c_name, g, s_range = current_key
            print(f"{c_name}\t{g}\t{s_range}\t{students_str}")

            # Reset
            current_key = key
            student_list = []

        # Add student to group
        student_list.append(student_name)

    # Output last group
    if current_key is not None:
        students_str = ", ".join(student_list)
        c_name, g, s_range = current_key
        print(f"{c_name}\t{g}\t{s_range}\t{students_str}")


if __name__ == "__main__":
    main()