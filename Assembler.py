# import files
import sys
import re
import json

# main
def main():

    check_input()

    with open( sys.argv[1], "r" ) as file:
        input_code_list = [ loc.split('#')[0].strip() 
                       for loc in file
                      if loc.split('#')[0].strip() != "" ]
    
    labels_dict = get_labels( input_code_list )

    binary_code_list = convert_to_binary( input_code_list, labels_dict )








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


# fn to return all the labels in the assembly code
def get_labels(code):
    labels = {}
    pc = 0
    for line_of_code in code:
        if ( match := re.match( r"^(\w+)\s*:(.*)", line_of_code ) ):
            label = match.group(1)
            rest_of_line = match.group(2).strip()

            if label in labels:
                sys.exit(f"Error: Duplicate label '{label}'")

            labels[label] = pc

            if rest_of_line: pc+=4

        else:
            pc+=4

    return labels


def convert_to_binary( code, labels ):
    with open("opcodes.json", "r") as f1:
        opcodes_dict = json.load(f1)

    binary_list = []
    line_number = 0
    pc = 0

    for line in code:
        line_number+=1
        
        if ( match := re.match( r"^(\w+)\s*:(.*)", line ) ):
            if match.group(2).strip() != "":
                line_of_code = match.group(2).strip()
            else:
                continue
        else:
            line_of_code = line
        
        elements = re.split(r'[ ,()]+', line_of_code)
        instruction = elements[0]
        instruction_data = opcodes_dict.get(instruction)

        if instruction not in opcodes_dict:
            sys.exit(f"Error: Unknown instruction '{instruction}' at line {line_number}" )

        match instruction_data["type"]:

            case "R":
                binary_line = get_R_type_binary()
            
            case "I":
                binary_line = get_I_type_binary()
            
            case "S":
                binary_line = get_S_type_binary()

            case "B":
                binary_line = get_B_type_binary()

            case "J":
                binary_line = get_J_type_binary()
            
            case _:
                binary_line = get_special_
            

            
    

    
    ...


if __name__ == "__main__":
    main()