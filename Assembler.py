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

    # Loading opcode and register data from json files 
    with open("opcodes.json", "r") as f1:
        opcodes_dict = json.load(f1)

    with open("registers.json", "r") as f2:
        registers_dict = json.load(f2)


    binary_list = []
    line_number = 0
    pc = 0

    # loop for checking each line from code for instrctions
    for line in code:
        line_number+=1
        
        # Using Regex to get instructions and remove any labels we had
        if ( match := re.match( r"^(\w+)\s*:(.*)", line ) ):
            if match.group(2).strip() != "":
                line_of_code = match.group(2).strip()
            else:
                continue
        else:
            line_of_code = line
        
        # Getting all the individual imm[11:0], opcodes, and operands in a list named elements
        elements = [i for i in re.split(r'[ ,()]+', line_of_code) if i!='']
        instruction = elements[0]
        instruction_data = opcodes_dict.get(instruction)

        # Exists program if opcode not found
        if instruction not in opcodes_dict:
            sys.exit(f"Error: Unknown instruction '{instruction}' at line {line_number}" )

        # Checking for instruction type
        match instruction_data["type"]:

            case "R":
                binary_line = get_R_type_binary(elements, opcodes_dict, registers_dict, line_number)
            
            case "I":
                binary_line = get_I_type_binary(elements, opcodes_dict, registers_dict, line_number)

            case "S":
                binary_line = get_S_type_binary(elements, opcodes_dict, registers_dict, line_number)

            case "B":
                print(get_labels)
                binary_line = get_B_type_binary(elements, opcodes_dict, registers_dict, line_number)

            case "J":
                binary_line = get_J_type_binary(elements, opcodes_dict, registers_dict, line_number)

            case _:
                binary_line = get_special_type_binary(elements, opcodes_dict, registers_dict, line_number)

        
        if binary_line: binary_list.append(binary_line)
        
# Function to check whether the immidiate value is a valid a valid INTEGER (doesn't check range)
def is_int(imm):
    imm=imm.removeprefix('-')

    if imm.isdigit():
        return 0
    return None

def get_R_type_binary(elements, opcodes_dict, registers_dict, line_number):
    
    # assigning and checking whether all the operands and opcode are present
    try:
        instruction, rd, rs1, rs2 = elements
    except ValueError:
        sys.exit(f"Error at line {line_number}: R-type instruction must have exactly 4 elements: instruction, rd, rs1, rs2")

    # checking whether the registers have valid names
    for reg in (rd, rs1, rs2):
        if reg not in registers_dict: 
            sys.exit(f"Error: Invalid register format '{reg}' at line {line_number}.")

    instruction_data = opcodes_dict.get(instruction)
  
    return f'{instruction_data["funct7"]} {registers_dict.get(rs2)} {registers_dict.get(rs1)} {instruction_data["funct3"]} {registers_dict.get(rd)} {instruction_data["opcode"]}'


def get_I_type_binary(elements, opcodes_dict, registers_dict, line_number):
    
    # Trying to get all the elements in seperate variables and exiting if instruction does not have exactly 4 elements 
    try:
        instruction, rd, rs1, imm = elements
        if is_int(rs1) == 0:
            temp = rs1
            rs1 = imm
            imm = temp
    except ValueError:
        sys.exit("Error: I-type instruction must have exactly 4 elements: instruction, rd, rs1, imm")

    # Exiting if imm is not an Integer
    if is_int(imm) == None:
        sys.exit(f"Error: Immediate value '{imm}' is not a valid number at line {line_number}.")
    
    # Exiting if imm is not in range
    if not (-2048 <= int(imm) <= 2047): 
        sys.exit(f"Error: Immediate value '{imm}' out of range (-2048 to 2047) at line {line_number}.")

    # Checking whether the registers have valid names
    if rs1 not in registers_dict or rd not in registers_dict:
        sys.exit(f"Error: Invalid register format '{rs1}' or '{rd}' at line {line_number}.")

    # Getting the binary form of imm (in 2's complement)
    imm = f"{int(imm) & 0b111111111111:012b}"
    instruction_data = opcodes_dict.get(instruction)

    return f'{imm} {registers_dict.get(rs1)} {instruction_data["funct3"]} {registers_dict.get(rd)} {instruction_data["opcode"]}'


def get_S_type_binary(elements, opcodes_dict, registers_dict, line_number):

    # Ensure correct format
    try:
        instruction, rs2, rs1, offset = elements 
        if is_int(rs1) == 0:
            temp = rs1
            rs1 = offset
            offset = temp
    except ValueError:
        sys.exit(f"Error at {line_number}: S-type instruction must have exactly 4 elements: instruction, rs2, offset, rs1")

    if rs1 not in registers_dict or rs2 not in registers_dict:
        sys.exit(f"Error: Invalid register format '{rs1}' or '{rs2}' at line {line_number}.")
    
    # Exiting if offset is not an Integer
    if is_int(offset) == None:
        sys.exit(f"Error: Immediate value '{offset}' is not a valid number at line {line_number}.")
    
    # Exiting if imm is not in range
    if not (-2048 <= int(offset) <= 2047): 
        sys.exit(f"Error: Immediate value '{offset}' out of range (-2048 to 2047) at line {line_number}.")

    instruction_data = opcodes_dict.get(instruction)

    # Getting offset value in 2's complement binary and splitting it into upper and lower
    imm_bin = f"{int(offset) & 0b111111111111:012b}"  
    imm_upper = imm_bin[:7] 
    imm_lower = imm_bin[7:]  

    return f'{imm_upper} {registers_dict[rs2]} {registers_dict[rs1]} {instruction_data["funct3"]} {imm_lower} {instruction_data["opcode"]}'

def get_B_type_binary(elements, opcodes_dict, registers_dict, line_number):
    
    # Ensure correct format
    try:
        instruction, rs2, rs1, offset = elements 
        if not rs1[1:].isdigit() and (rs1[0] == '-' or rs1[0].isdigit()):
            temp = rs1
            rs1 = offset
            offset = temp
    except ValueError:
        sys.exit(f"Error at {line_number}: B-type instruction must have exactly 4 elements: instruction, rs2, offset, rs1")

    # Checking whether the registers have valid names
    if rs1 not in registers_dict or rs2 not in registers_dict:
        sys.exit(f"Error: Invalid register format '{rs1}' or '{rs2}' at line {line_number}.")

    # 
    try:
        imm = int(offset)
        if not (-2048 <= imm <= 2047): 
            sys.exit(f"Error: Immediate value '{imm}' out of range (-2048 to 2047) at line {line_number}.")
    except ValueError:
        sys.exit(f"Error: Immediate value '{offset}' is not a valid number at line {line_number}.")

    instruction_data = opcodes_dict.get(instruction)
    imm_bin = f"{int(imm) & 0b111111111111:012b}"  
    imm_upper = imm_bin[:7] 
    imm_lower = imm_bin[7:]  

    return f'{imm_upper} {registers_dict[rs2]} {registers_dict[rs1]} {instruction_data["funct3"]} {imm_lower} {instruction_data["opcode"]}'



def get_J_type_binary():
    ...
def get_special_type_binary():
    ...



if __name__ == "__main__":
    main()