import sys


def main():

    current_key = None
    total_count = 0

    for line in sys.stdin:

        # Remove whitespace
        line = line.strip()


        # Split mapper output
        key, value = line.split("\t", 1)

        # Convert value to integer
        try:
            value = int(value)
        except ValueError:
            continue

        # First key
        if current_key is None:
            current_key = key

        # Same key
        if key == current_key:
            total_count += value

        # New key 
        else:
            print(f"{current_key}\t{total_count}")

            current_key = key
            total_count = value

    # Output last key
    if current_key is not None:
        print(f"{current_key}\t{total_count}")


if __name__ == "__main__":
    main()