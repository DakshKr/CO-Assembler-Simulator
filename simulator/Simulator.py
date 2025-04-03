import sys
import re
import numpy as np
import cowsay

def main():
    check_input()

    # Read input file lines into a list named "program"
    with open(sys.argv[1], "r") as file:
        program = [l.strip() for l in file if l.strip()]

    register_arr = np.zeros(32, dtype=int)
    output = []  # List for logging register state
    register_arr[2] = 380
    memory = {
    "0x00010000": 0, "0x00010004": 0, "0x00010008": 0, "0x0001000C": 0,
    "0x00010010": 0, "0x00010014": 0, "0x00010018": 0, "0x0001001C": 0,
    "0x00010020": 0, "0x00010024": 0, "0x00010028": 0, "0x0001002C": 0,
    "0x00010030": 0, "0x00010034": 0, "0x00010038": 0, "0x0001003C": 0,
    "0x00010040": 0, "0x00010044": 0, "0x00010048": 0, "0x0001004C": 0,
    "0x00010050": 0, "0x00010054": 0, "0x00010058": 0, "0x0001005C": 0,
    "0x00010060": 0, "0x00010064": 0, "0x00010068": 0, "0x0001006C": 0,
    "0x00010070": 0, "0x00010074": 0, "0x00010078": 0, "0x0001007C": 0
    }


    pc = 0

    while True:
        # print(pc//4 + 1,"\n",memory,"\n\n")
        if pc // 4 >= len(program):
            sys.exit("\nError: program counter out-of-bounds\n")

        binary_line = program[pc // 4]
        opcode = binary_line[-7:]

        if binary_line == "00000000000000000000000001100011": # HALT
            output.append(get_log(pc, register_arr))
            break

        match opcode:
            # R-Type instructions
            case "0110011":
                rs1 = int(binary_line[12:17], 2)
                rs2 = int(binary_line[7:12], 2)
                rd = int(binary_line[20:25], 2)
                func3 = binary_line[17:20]
                
                if rd != 0:
                    match func3:
                        case "000":
                            func7 = binary_line[:7]
                            if func7 == "0100000":
                                register_arr[rd] = register_arr[rs1] - register_arr[rs2]
                            elif func7 == "0000000":
                                register_arr[rd] = register_arr[rs1] + register_arr[rs2]
                            else:
                                sys.exit(f"Unknown R-Type Instruction at line {pc // 4 + 1}")
                        case "010":
                            register_arr[rd] = 1 if register_arr[rs1] < register_arr[rs2] else 0
                        case "100":
                            register_arr[rd] = register_arr[rs1] ^ register_arr[rs2]
                        case "101":
                            # Get the lower 5 bits of rs2 as the shift amount
                            shift_amount = register_arr[rs2] & 0b11111
                            func7 = binary_line[:7]
                            if func7 == "0100000":
                                # Arithmetic right shift (SRA)
                                register_arr[rd] = register_arr[rs1] >> shift_amount
                            elif func7 == "0000000":
                                # Logical right shift (SRL): mask to 32 bits first
                                register_arr[rd] = (register_arr[rs1] & 0xFFFFFFFF) >> shift_amount
                            else:
                                sys.exit(f"Unknown R-Type Instruction at line {pc // 4 + 1}")
                        case "110":
                            register_arr[rd] = register_arr[rs1] | register_arr[rs2]
                        case "111":
                            register_arr[rd] = register_arr[rs1] & register_arr[rs2]
                        case _:
                            sys.exit(f"Unknown R-Type Instruction at line {pc // 4 + 1}")

                    # Ensure x0 remains 0
                    register_arr[0] = 0
                    pc += 4

            # B-Type instructions (branches)
            case "1100011":
                imm = sign_extend(binary_line[0] + binary_line[24] + binary_line[1:7] + binary_line[20:24] + "0", 13)
                rs1 = int(binary_line[12:17], 2)
                rs2 = int(binary_line[7:12], 2)
                func3 = binary_line[17:20]
                match func3:
                    case "000":
                        pc += imm if register_arr[rs1] == register_arr[rs2] else 4
                    case "001":
                        pc += imm if register_arr[rs1] != register_arr[rs2] else 4
                    case "100":
                        pc += imm if register_arr[rs1] < register_arr[rs2] else 4
                    case "101":
                        pc += imm if register_arr[rs1] >= register_arr[rs2] else 4
                    case _:
                        sys.exit(f"Unknown B-Type Instruction at line {pc // 4 + 1}")

            # Special-Type instructions (e.g., multiplication)
            case "1111111":
                rs1 = int(binary_line[12:17], 2)
                rs2 = int(binary_line[7:12], 2)
                rd = int(binary_line[20:25], 2)
                func3 = binary_line[17:20]
                if rd == 0:
                    pc += 4
                    continue

                if func3 == "100":
                    register_arr[rd] = register_arr[rs1] * register_arr[rs2]
                elif func3 == "010":
                    register_arr = np.zeros(32, dtype=int)
                else:
                    sys.exit(f"Unknown Special-Type Instruction at line {pc // 4 + 1}")

                # Ensure x0 remains 0 and increment pc
                register_arr[0] = 0
                pc += 4

            # S-Type instructions (stores)
            case "0100011":
                
                imm = sign_extend(binary_line[:7] + binary_line[20:25], 12)
                rs1 = int(binary_line[12:17], 2)
                rs2 = int(binary_line[7:12], 2)
                address = register_arr[rs1] + imm
                if address % 4 != 0 or address < 0:
                    sys.exit(f"Invalid Address at line {pc // 4 + 1}")
                
                memory[decimal_to_hex(address)] = register_arr[rs2]
                pc += 4

            # J-Type instructions (jump and link)
            case "1101111":
                rd = int(binary_line[20:25], 2)
                imm = sign_extend(binary_line[0] + binary_line[12:20] + binary_line[11] + binary_line[1:11] + "0", 21)
    
                if rd != 0:
                    register_arr[rd] = (pc + 4)
                register_arr[0] = 0
                pc += imm

            # I-Type instructions: addi
            case "0010011":
                rd = int(binary_line[20:25], 2)
                rs1 = int(binary_line[12:17], 2)
                func3 = binary_line[17:20]

                if func3 != "000":
                    sys.exit(f"Unknown I-Type Instruction at line {pc // 4 + 1}")

                imm = get_signed_int(binary_line[:12])
                if rd != 0:
                    register_arr[rd] = register_arr[rs1] + imm
                register_arr[0] = 0
                pc += 4

            # I-Type instruction: lw 
            case "0000011":
                rd = int(binary_line[20:25], 2)
                rs1 = int(binary_line[12:17], 2)
                imm = sign_extend(binary_line[:12], 12)
                address = register_arr[rs1] + imm

                if address % 4 != 0 or address < 0:
                    sys.exit(f"Invalid memory access at line {pc // 4 + 1}")

                register_arr[rd] = memory[decimal_to_hex(address)]
                register_arr[0] = 0
                pc += 4

            # I-Type instruction: jalr
            case "1100111":
                rd = int(binary_line[20:25], 2)
                rs1 = int(binary_line[12:17], 2)
                func3 = binary_line[17:20]

                if func3 != "000":
                    sys.exit(f"Unknown I-Type Instruction at line {pc // 4 + 1}")
                                
                imm = sign_extend(binary_line[:12], 12)
                return_address = pc + 4

                # Set PC to (register_arr[rs1] + imm) with LSB forced to 0.
                pc = (register_arr[rs1] + imm) & ~1
                if rd != 0:
                    register_arr[rd] = return_address

                # Enforce that x0 is always 0.
                register_arr[0] = 0

            
        output.append(get_log(pc, register_arr))

        # print(pc, register_arr)
    # Write logs and memory contents to the output file
    with open(sys.argv[2], "w") as f:
        for log in output:
            f.write(log + "\n")
        # for i in range(len(memory)):
        #     f.write( addresses[i]+":" + i_to_b(str(memory[i])) + "\n")
        m = list(memory.keys())[:32]
        for address in m:
            f.write(f"{address}:{i_to_b(memory[address])}\n")
    
    cowsay.cow('Success')

def check_input():
    if len(sys.argv) != 3:
        sys.exit("\nMissing/Exceeding the number of Command Line Arguments\n\n")
    if not re.fullmatch(r"^[a-zA-Z0-9_/\\.-]+\.txt$", sys.argv[1]):
        sys.exit("\nInvalid Input File Path\n\n")
    if not re.fullmatch(r"^[a-zA-Z0-9_/\\.-]+\.txt$", sys.argv[2]):
        sys.exit("\nInvalid Output File Path\n\n")
    try:
        with open(sys.argv[1], "r") as f:
            pass
    except FileNotFoundError:
        sys.exit("\nInput File Not Found\n\n")
    if sys.argv[1] == sys.argv[2]:
        sys.exit("\nInput & Output File Can't be same\n\n")

def i_to_b(integer):
    return f"0b{int(integer) & 0xFFFFFFFF:032b}"

def get_log(pc, r_list):
    transe = i_to_b(pc)
    for reg in r_list:
        transe += f" {i_to_b(reg)}"
    return transe

def sign_extend(value, bits):
    if value[0] == "1":
        return int(value, 2) - (1 << bits)    
    return int(value, 2)

def decimal_to_hex(decimal):
    return f"0x{decimal & 0xFFFFFFFF:08X}"

def get_signed_int(str1: str) -> int:
    if str1[0] == "0":
        return int(str1, 2)
    else:
        str2 = ''
        for i in str1:
            str2+="1" if i == "0" else "0"
        return -1 * (int(str2, 2) + 1)

if __name__ == "__main__":
    main()