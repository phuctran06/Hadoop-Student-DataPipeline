import sys


def output_result(key, total_count, pass_count, fail_count):
    semester, year = key
    pass_rate = (pass_count / total_count) * 100 if total_count else 0
    fail_rate = (fail_count / total_count) * 100 if total_count else 0
    print(f"{semester}\t{year}\t{total_count}\t{pass_count}\t{fail_count}\t{pass_rate:.2f}\t{fail_rate:.2f}")


def main():

    current_key = None
    total_count = 0
    pass_count = 0
    fail_count = 0

    for line in sys.stdin:

        semester, year, result = line.rstrip("\n").split("\t")

        key = (semester, year)

        # Check new group
        if current_key is None:
            current_key = key

        if key != current_key:

            # Output result
            output_result(current_key, total_count, pass_count, fail_count)

            # Reset
            current_key = key
            total_count = 0
            pass_count = 0
            fail_count = 0

        total_count += 1
        if result == "Pass":
            pass_count += 1
        else:
            fail_count += 1

    # Output last group
    if current_key is not None:
        output_result(current_key, total_count, pass_count, fail_count)


if __name__ == "__main__":
    main()