import argparse
import re
# Constants
instruction_map = {
    "add": {
        "opcode": "0000",
        "subop": "0",
        "format": "R",
        "num_operands": 2
    },
    "addi": {
        "opcode": "0001",
        "subop": "X",
        "format": "I",
        "num_operands": 2
    },
    "addui": {
        "opcode": "0001",
        "subop": "X",
        "format": "I",
        "num_operands": 2
    },
    "mult": {
        "opcode": "0010",
        "subop": "0",
        "format": "R",
        "num_operands": 2
    },
    "lw": {
        "opcode": "0110",
        "subop": "0",
        "format": "R",
        "num_operands": 2
    },
    "sw": {
        "opcode": "0110",
        "subop": "1",
        "format": "R",
        "num_operands": 2
    },
    "halt": {
        "opcode": "0111",
        "subop": "0",
        "format": "R",
        "num_operands": 0
    },
    "bz": {
        "opcode": "1000",
        "subop": "X",
        "format": "I",
        "num_operands": 2
    },
    "bp": {
        "opcode": "1010",
        "subop": "X",
        "format": "I",
        "num_operands": 2
    },
    "put": {
        "opcode": "1111",
        "subop": "X",
        "format": "I",
        "num_operands": 1
    }

}

reg_map = {
    "$r0": "000",
    "$r1": "001",
    "$r2": "010",
    "$r3": "011",
    "$r4": "100",
    "$r5": "101",
    "$r6": "110",
    "$r7": "111"
}


def binary_string(num, length):
    bin_string = '{:0{}b}'.format(num, length)
    return bin_string.split('b')[-1]


def convert_instruction(line):

    # Split args by space
    instruct_tokens = re.split('[ ,]',line)

    # Remove any unwanted space tokens
    clean_tokens = []
    for token in instruct_tokens:
        if re.search('\w',token):
            clean_tokens.append(token)
    instruct_tokens = clean_tokens




    # Get main instruction
    instruction = instruct_tokens[0]

    # Get format
    instruct_fmt = instruction_map[instruction]

    # Opcode will always be present
    opcode = instruct_fmt["opcode"]

    # Return
    instruction_bin = ""

    if instruct_fmt["format"] == "R":
        subop = instruct_fmt["subop"]

        # Special case for halt
        if instruct_fmt["num_operands"] == 0:
            rs = "000"
            rt = "000"
        # Normal instruction with rs and rt
        else:
            rs = reg_map[instruct_tokens[1]]
            rt = reg_map[instruct_tokens[2]]

        instruction_bin = convert_r_hex(opcode, subop, rs, rt)
    # I-type
    else:
        # All I instructions have rs
        rs = reg_map[instruct_tokens[1]]
        unsigned = "1" if instruction == "addui" else "0"
        binary_imm = "00000000"

        if instruct_fmt["num_operands"] == 2:
            binary_imm = binary_string(int(instruct_tokens[2]), 8)

        instruction_bin = convert_i_hex(opcode, rs, unsigned, binary_imm)

    instruction_hex = format(int(instruction_bin, 2), '04x').upper()

    print("\nInstruction: " + line)
    print("\tBinary: " + instruction_bin)
    print("\tHex: " + instruction_hex)

    return instruction_hex


def convert_r_hex(opcode, subop, rs="000", rt="000", shamt="0000"):
    return opcode + rs + rt + "0" + shamt + subop


def convert_i_hex(opcode, rs, unsigned, imm):
    return opcode + rs + unsigned + imm


def compile(file_name):
    # Generate compile filename
    out_file_name = file_name.split('.')[0] + '-compiled.txt'

    print("Compiling " + file_name + " to " + out_file_name + "...")

    # Open file pointers
    out_fp = open(out_file_name, 'w')
    in_fp = open(file_name, 'r')

    # Write opening line
    write_line(out_fp, 'v2.0 raw')

    # Parse input file
    in_lines = in_fp.readlines()
    in_fp.close()
    for in_line in in_lines:
        in_line = in_line.strip('\n')
        # Avoid comments
        if in_line.startswith("#") or in_line == "":
            continue
        hex_instruction = convert_instruction(in_line)
        write_line(out_fp, hex_instruction)

    out_fp.close()
    in_fp.close()


def write_line(fp, line):
    fp.write(line + '\n')


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("mipsfile", help="File containing MIPS instruction",
                        type=str)
    args = parser.parse_args()

    compile(args.mipsfile)

    print("\n**** Done **** \n")
