# import files
import sys
import re
import json
import numpy as np

# main
def main():

    check_input()

    # getting data from a the input file in a list named "program"
    with open( sys.argv[1], "r" ) as file:
        program = [l.strip() for l in file if l.strip()]

    register_arr = np.zeros(32, dtype=int)
    memory = np.zeros(32, dtype=int)
    output = []   # not using array here due to efficiency (appending multiple targets)
    pc = 0
    

    while True:

        if pc//4 >= len(program):
            sys.exit("\nError: program counter out-of-bounds\n")

        binary_line = program[pc//4]
        opcode = binary_line[-7:]

        output.append(get_log(pc, register_arr))
        
        match opcode:

            # for r-type
            case "0110011":
                rs1 = int(binary_line[12:17], 2)
                rs2 = int(binary_line[7:12], 2)
                rd = int(binary_line[20:25], 2)
                func3 = binary_line[17:20]
                if rd == 0:
                    continue

                match func3:

                    case "000":
                        func7 = binary_line[:7]
                        if func7 == "0100000":
                            register_arr[rd] = register_arr[rs1] - register_arr[rs2]
                        elif func7 == "0000000":
                            register_arr[rd] = register_arr[rs1] + register_arr[rs2]
                        else:
                            sys.exit(f"Unknown R-Type Instruction at line {pc//4}")
                    
                    case "010":
                        register_arr[rd] = 1 if register_arr[rs1] < register_arr[rs2] else 0

                    case "101":
                        shift = -1 * int(register_arr[rs2][-5:] , 2)
                        register_arr[rd] = f"{0*shift}{register_arr[rs1][:shift]}"

                    case "110":
                        register_arr[rd] = register_arr[rs1] | register_arr[rs2]

                    case "111":
                        register_arr[rd] = register_arr[rs1] & register_arr[rs2]

                    case "100":
                         register_arr[rd] = register_arr[rs1] ^ register_arr[rs2]
                    
                    case _:
                        sys.exit(f"Unknown R-Type Instruction at line {pc//4}")
                    



                func3 =    binary_line

            # for b-type
            case "1100011":
                ...         
            
            case "1111111":
                ...         # for special-type
            
            case "0100011":
                ...         # for s-type
            
            case "1101111":
                ...         # for j-type
            
            case _:
                ...         # for i-type
                








# fn to check whether the user gave valid CLIs
def check_input():

    # make sure that the user gave both the input file and output file
    if len( sys.argv ) != 3:
        sys.exit( "\nMissing/Exceeding the number of Command Line Arguments\n\n" )

    # checks whether the input file name is valid
    if not re.fullmatch( r"^[a-zA-Z0-9_/\\.-]+\.txt$", sys.argv[1] ):
        sys.exit( "\nInvalid Input File Path\n\n" )

    # checks whether the output file name is valid
    if not re.fullmatch( r"^[a-zA-Z0-9_/\\.-]+\.txt$", sys.argv[2] ):
        sys.exit( "\nInvalid Output File Path\n\n" )

    # make sures whether the input file exists
    try:
        with open( f"{sys.argv[1]}", "r" ) as f:
            pass
    except FileNotFoundError:
        sys.exit( "\nInput File Not Found\n\n" )

    if sys.argv[1] == sys.argv[2]:
        sys.exit( "\nInput & Output File Can't be same\n\n" )

def i_to_b(integer):
    return f"0b{int(integer) & 0b111111111111:032b}"

def get_log(pc,r_list):
    transe = i_to_b(pc)
    for reg in r_list:
        transe += f" {i_to_b(reg)}"
    return transe


if __name__ == "__main__":
    main()