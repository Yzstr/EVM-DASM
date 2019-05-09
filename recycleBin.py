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