def main():
    # Hardcoded file names
    file1 = "out.txt"
    file2 = "correct_binary.txt"

    try:
        with open(file1, 'r') as f1:
            lines1 = f1.readlines()
        with open(file2, 'r') as f2:
            lines2 = f2.readlines()
    except Exception as e:
        print("Error reading files:", e)
        return

    mismatch_found = False
    min_lines = min(len(lines1), len(lines2))

    print("Mismatched lines:")
    for i in range(min_lines):
        if lines1[i].strip() != lines2[i].strip():
            print(f"Line {i+1}:")
            print(f"  File1: {lines1[i].rstrip()}")
            print(f"  File2: {lines2[i].rstrip()}")
            mismatch_found = True

    # Check if one file has extra lines
    if len(lines1) != len(lines2):
        mismatch_found = True
        print("\nExtra lines in one of the files:")
        if len(lines1) > min_lines:
            for i in range(min_lines, len(lines1)):
                print(f"  File1 Line {i+1}: {lines1[i].rstrip()}")
        else:
            for i in range(min_lines, len(lines2)):
                print(f"  File2 Line {i+1}: {lines2[i].rstrip()}")

    if not mismatch_found:
        print("All lines match.")

if __name__ == '__main__':
    main()
