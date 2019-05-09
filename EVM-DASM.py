from MAP import *






def get_opcode(string):
    skip_times = 0
    first_stop = 0
    log_out = False
    last_stop = 0

    print_gap(0)
    for _ in range(2):
        for i in range(0, len(string), 2):
            code = string[i:i+2]
            if skip_times != 0:
                if log_out:
                    print(code, end='')
                skip_times -= 1
                if skip_times == 0:
                    if log_out:
                        print('')
                continue

            if code == '00':
                if first_stop == 0:
                    first_stop = i
                if not log_out:
                    last_stop = i
                else:
                    print(code+": "+opcodes[code])
                    if i == first_stop:
                        print_gap(1)
                    if i == last_stop:
                        break
                    continue

            if code[0] != '6' and code[0] != '7':
                if code in opcodes.keys():
                    if log_out:
                        print(code+": "+opcodes[code])
                else:
                    if log_out:
                        print(code+': <------------ ERROR')
                        print('The Contract Opcode ends at {}.\\'.format(last_stop))
                    break

            else:
                n = push_map[code]

                if log_out:
                    print(code+": PUSH"+str(n)+" ", end='')
                skip_times = n

        log_out = True
        # print(last_stop)

    data = string[last_stop:]
    bzzr_begin = data.find('a165627a7a72305820')
    if log_out:
        print_gap(2)
        print(data[:bzzr_begin], end='\n\n')

    if bzzr_begin > -1:
        if log_out:
            print_gap(3)
            print("bzzr: "+data[bzzr_begin+18:bzzr_begin+18+64])
        abi_begin = bzzr_begin+18+64+4
        print_gap(4)
        for i in range(abi_begin, len(data), 64):
            if log_out:
                print('Arg [{}]: '.format(str(i // 64))+data[i:i+64])
    else:
        if log_out:
            print('bzzr not found')


def split_byteCode(byteCode,isDeploy=True):
    contract_start=0
    contract_end=0
    bzzr_start=0
    augs_start=0
    deployment=''
    contract=''
    bzzr=''
    augs=[]

    byteCode=byteCode.lower()
    if isDeploy:
        contract_start=byteCode.find('f300')
        contract_start+=4

    bzzr_start=byteCode.find('a165627a7a72305820')
    bzzr='bzzr: '+byteCode[bzzr_start+18:bzzr_start+18+64]
    augs_start=bzzr_start+18+64+4

    for i in range(augs_start,len(byteCode),64):
        aug=str('Arg [{}]: '.format(str((i-augs_start) // 64))+byteCode[i:i+64])
        augs.append(aug)
    deployment=byteCode[:contract_start]
    contract=byteCode[contract_start:bzzr_start]
    return deployment,contract,bzzr,augs
    

def get_opCode_list(byteCode):
    opCode_list=[]
    push_skip_times=0
    for i in range(0,len(byteCode),2):
        code=byteCode[i:i+2]
        if push_skip_times==0:
            if code[0] != '6' and code[0] != '7':
                opCode=code+':  '+opcodes[code]
                opCode_list.append(opCode)
            else:
                push_skip_times=push_map[code]
                opCode=code+':  '+opcodes[code]+'       '+byteCode[i+2:i+2+push_skip_times*2]
                opCode_list.append(opCode)
        else:
            push_skip_times-=1
            continue
    return opCode_list






if __name__ == "__main__":
    hex_string = input("Bytecode(hex):")
    get_opcode(hex_string)
