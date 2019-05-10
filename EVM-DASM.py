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
    augs_start = 0
    deployment = ''
    contract = ''
    bzzr = ''
    augs = []

    byteCode = byteCode.lower()
    if isDeploy:
        contract_start = byteCode.find('f300')
        contract_start += 4

    bzzr_start = byteCode.find('a165627a7a72305820')
    bzzr = 'bzzr: '+byteCode[bzzr_start+18:bzzr_start+18+64]
    augs_start = bzzr_start+18+64+4

    for i in range(augs_start, len(byteCode), 64):
        aug = str('Arg [{}]: '.format(
            str((i-augs_start) // 64))+byteCode[i:i+64])
        augs.append(aug)
    deployment = byteCode[:contract_start]
    contract = byteCode[contract_start:bzzr_start]
    return deployment, contract, bzzr, augs


def get_opCode_list(byteCode):
    opCode_list = []
    push_skip_times = 0
    for i in range(0, len(byteCode), 2):
        code = byteCode[i:i+2]
        if push_skip_times == 0:
            loc = '0x'+str(hex(i//2))[2:].zfill(8)
            if code[0] != '6' and code[0] != '7':
                opCode = [loc, code, opCodes.get(code, '<------- ERROR'), '']
                opCode_list.append(opCode)
            else:
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
        for opCode in opCode_list:
            print(opCode[0]+':  '+opCode[1]+'   ' +
                  opCode[2]+'       '+opCode[3])
        print('\n\n\n')
    else:
        for i in range(len(opCode_list)):
            if opCode_list[i][1] == '80':
                if opCode_list[i+1][1] == '63' and opCode_list[i+2][1] == '14' and opCode_list[i+3][1] == '61' and opCode_list[i+4][1] == '57':
                    function_name_hash = opCode_list[i+1][3]
                    function_name = abi_hash_dict[function_name_hash][0]
                    abi_hash_dict[function_name_hash][1] = opCode_list[i+3][3]
                    print('\nFunction Head:   '+function_name)
            function_check = get_function_name_by_address(
                opCode_list[i][0][-4:], abi_hash_dict)
            if function_check != None:
                print('\nFunction Body:   '+function_check)
            print(opCode_list[i][0]+':  '+opCode_list[i][1] +
                  '   '+opCode_list[i][2]+'       '+opCode_list[i][3])
            if opCode_list[i][1] == '00' or opCode_list[i][1] == 'f3':
                print('\n')
        print('\n\n\n')


def get_function_name_by_address(address, abi_hash_dict):
    for abi_info in abi_hash_dict.values():
        if address == abi_info[1]:
            return abi_info[0]
    return None


def get_abi_hash_dict(abi_file):
    with open(abi_file, 'r') as f:
        abi_data_all = json.load(f)

    function_name_list = []

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

    deployment, contract, bzzr, augs = split_byteCode(binary_file)

    deploy_list = get_opCode_list(deployment)
    contract_list = get_opCode_list(contract)

    print_opCode(deploy_list)
    print_opCode(contract_list, abi_hash_dict, True)

    
    pprint(abi_hash_dict)
    print('\n\n')
    pprint(bzzr)
    print('\n\n')
    pprint(augs)
