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

    match_found = False
    # Compare line by line up to the smaller file's length
    min_lines = min(len(lines1), len(lines2))
    print("Matching lines:")
    for i in range(min_lines):
        # Strip newline and extra whitespace for an accurate comparison
        if lines1[i].strip() == lines2[i].strip():
            print(f"Line {i+1}: {lines1[i].rstrip()}")
            match_found = True

    if not match_found:
        print("No matching lines found.")

if __name__ == '__main__':
    main()
