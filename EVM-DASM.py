from MAP import *
import sys
import json
import sha3
from pprint import pprint


def split_byteCode(byteCode_file, isDeploy=True):
    with open(byteCode_file, 'r') as f:
        byteCode = f.read()
    contract_start = 0
    contract_end = 0       # How to find the end if the end is not the begin of bzzr?
    bzzr_start = 0
    args_start = 0
    deployment = ''
    contract = ''
    bzzr = ''
    args = []

    byteCode = byteCode.lower()
    if isDeploy:
        contract_start = byteCode.find('f300') + 4

    bzzr_start = byteCode.find('a165627a7a72305820')+18
    bzzr = 'bzzr: '+byteCode[bzzr_start:bzzr_start+64]
    args_start = bzzr_start+64+4

    for i in range(args_start, len(byteCode), 64):
        aug = str('Arg [{}]: '.format(
            str((i-args_start) // 64))+byteCode[i:i+64])
        args.append(aug)

    deployment = byteCode[:contract_start]
    contract = byteCode[contract_start:bzzr_start]
    return deployment, contract, bzzr, args


def get_opCode_list(byteCode):
    """
    input: byteCode -> string
    output: opCode List -> list of lists

    Structure of an opCode: [address, bytecode, opcode, arguments if exist]
    """

    opCode_list = []
    push_skip_times = 0
    for i in range(0, len(byteCode), 2):
        code = byteCode[i:i+2]
        if push_skip_times == 0:
            loc = '0x'+str(hex(i//2))[2:].zfill(8)
            if code[0] != '6' and code[0] != '7':
                # is not a push-like opCode
                opCode = [loc, code, opCodes.get(code, '<------- ERROR'), '']
                opCode_list.append(opCode)
            else:
                # is a push-like opCode
                push_skip_times = push_map[code]
                opCode = [loc, code, opCodes.get(
                    code, '<------- ERROR'), byteCode[i+2:i+2+push_skip_times*2]]
                opCode_list.append(opCode)
        else:
            push_skip_times -= 1
            continue
    return opCode_list


def print_opCode(opCode_list, abi_hash_dict={}, isContract=False):
    if not isContract:
        # print the deployment opCode, just print it all
        for opCode in opCode_list:
            print(opCode[0]+':  '+opCode[1]+'   ' +
                  opCode[2]+'       '+opCode[3])
        print('\n\n\n')
    else:
        for i in range(len(opCode_list)):
            if opCode_list[i][1] == '80':
                if opCode_list[i+1][1] == '63' and opCode_list[i+2][1] == '14' and (opCode_list[i+3][1] in push_map.keys()) and opCode_list[i+4][1] == '57':
                    # found a function head here
                    function_name_hash = opCode_list[i+1][3]
                    function_name = abi_hash_dict[function_name_hash][0]
                    # put the function address to abi_hash_dict
                    abi_hash_dict[function_name_hash][1] = opCode_list[i+3][3]
                    print('\nFunction Head:   '+function_name)
            # check if it is a function body
            function_check = get_function_name_by_address(
                opCode_list[i][0], abi_hash_dict)
            if function_check:
                print('\nFunction Body:   '+function_check)
            print(opCode_list[i][0]+':  '+opCode_list[i][1] +
                  '   '+opCode_list[i][2]+'       '+opCode_list[i][3])
            if opCode_list[i][1] == '00' or opCode_list[i][1] == 'f3':
                print('\n')
        print('\n\n\n')


def get_function_name_by_address(address, abi_hash_dict):
    for abi_info in abi_hash_dict.values():
        if address[-1*len(abi_info[1]):] == abi_info[1] and address[2:-1*len(abi_info[1])] == (8-len(abi_info[1]))*'0':
            return abi_info[0]
    return None


def get_abi_hash_dict(abi_file):
    with open(abi_file, 'r') as f:
        abi_data_all = json.load(f)

    function_name_list = []

    # construct function name as 'foo(type1, type2, ... , typen)'
    for abi_data in abi_data_all:
        if abi_data['type'] == 'function':
            name = abi_data['name']
            name += '('
            if not abi_data['inputs']:
                name += ')'
            else:
                for input_aug in abi_data['inputs']:
                    name += input_aug['type']
                    name += ','
                name = name[:-1]
                name += ')'
            function_name_list.append(name)
    abi_hash_dict = {}
    for name in function_name_list:
    # get hashed function name using keccak_256
        hashed_string = sha3.keccak_256(
            name.encode('utf-8')).hexdigest().lower()[:8]
        abi_hash_dict[hashed_string] = [name, '']
    return abi_hash_dict


if __name__ == "__main__":
    binary_file = sys.argv[1]
    abi_file = sys.argv[2]

    abi_hash_dict = get_abi_hash_dict(abi_file)

    pprint(abi_hash_dict)
    print('\n\n')

    deployment, contract, bzzr, args = split_byteCode(binary_file)

    deploy_list = get_opCode_list(deployment)
    contract_list = get_opCode_list(contract)

    print_opCode(deploy_list)
    print_opCode(contract_list, abi_hash_dict, True)

    pprint(abi_hash_dict)
    print('\n\n')
    pprint(bzzr)
    print('\n\n')
    pprint(args)
