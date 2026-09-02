import sys


def output_result(course_id, count, sum_mid, sum_final, sum_total):
    avg_mid = sum_mid / count if count else 0
    avg_final = sum_final / count if count else 0
    avg_total = sum_total / count if count else 0
    print(f"{course_id}\t{count}\t{avg_mid:.2f}\t{avg_final:.2f}\t{avg_total:.2f}")


def main():
    current_key = None
    count = 0
    sum_mid = 0.0
    sum_final = 0.0
    sum_total = 0.0

    for line in sys.stdin:
        course_id, midterm, final_score, total_score = line.rstrip("\n").split("\t")
        key = course_id

        # Check new group
        if current_key is None:
            current_key = key

        if key != current_key:
            # Output result
            output_result(current_key, count, sum_mid, sum_final, sum_total)
            # Reset
            current_key = key
            count = 0
            sum_mid = 0.0
            sum_final = 0.0
            sum_total = 0.0

        count += 1
        sum_mid += float(midterm)
        sum_final += float(final_score)
        sum_total += float(total_score)

    # Output last group
    if current_key is not None:
        output_result(current_key, count, sum_mid, sum_final, sum_total)


if __name__ == "__main__":
    main()