# import files
import sys
import re

# main
def main():

    check_input()


    ...

# fn to check whether the user gave valid CLIs
def check_input():

    # make sure that the user gave both the input file and output file
    if len( sys.argv ) != 3:
        sys.exit( "\nMissing/Exceeding the number of Command Line Arguments\n\n" )

    # checks whether the input file name is valid
    if not re.fullmatch( r"^.+\.txt$", sys.argv[1] ):
        sys.exit( "\nInvalid Input File Name\n\n" )

    # checks whether the input file name is valid
    if not re.fullmatch( r"^.+\.txt$", sys.argv[2] ):
        sys.exit( "\nInvalid Output File Name\n\n" )

    # make sures whether the input file exists
    try:
        f = open( f"{sys.argv[1]}", "r" )
        f.close()
    except FileNotFoundError:
        sys.exit( "\nInput File Not Found\n\n" )

    if sys.argv[1] == sys.argv[2]:
        sys.exit( "\nInput & Output File Can't be same\n\n" )


if __name__ == "__main__":
    main()
