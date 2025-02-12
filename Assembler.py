# import files
import sys
import re

# main
def main():

    check_input()


    ...

# fn to check whether the user gave valid command line arguments
def check_input():

    # make sure that the user gave both the input file and output file
    if len(sys.argv) != 3:
        sys.exit("Missing Command Line Argument")

    # checks whether the input file name is valid
    if not re.fullmatch(r"^.+\.txt$", sys.argv[1]):
        sys.exit("Invalid Input File Name")

    # checks whether the input file name is valid
    if not re.fullmatch(r"^.+\.txt$", sys.argv[2]):
        sys.exit("Invalid Output File Name")

    # make sures whether the input file exists
    try:
        f = open(f"{sys.argv[1]}", 'r')
    except FileNotFoundError:
        sys.exit("Input File Not Found")


if __name__ == "__main__":
    main()
