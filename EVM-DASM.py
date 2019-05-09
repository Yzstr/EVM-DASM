from MAP import *
import sys



def split_byteCode(byteCode,isDeploy=True):
    contract_start=0
    contract_end=0       # How to find the end if the end is not the begin of bzzr?
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
            loc='0x'+str(hex(i//2))[2:].zfill(8)
            if code[0] != '6' and code[0] != '7':
                opCode=[loc,code,opCodes.get(code,'<------- ERROR'),'']
                opCode_list.append(opCode)
            else:
                push_skip_times=push_map[code]
                opCode=[loc,code,opCodes.get(code,'<------- ERROR'),byteCode[i+2:i+2+push_skip_times*2]]
                opCode_list.append(opCode)
        else:
            push_skip_times-=1
            continue
    return opCode_list


def print_opCode(opCode_list):
    for opCode in opCode_list:
        print(opCode[0]+':  '+opCode[1]+'   '+opCode[2]+'       '+opCode[3])
    print('\n\n\n')








if __name__ == "__main__":
    binary_file=sys.argv[1]
    with open(binary_file,'r') as f:
        binary=f.read()
    
    deployment,contract,bzzr,augs=split_byteCode(binary)
    deploy_list=get_opCode_list(deployment)
    contract_list=get_opCode_list(contract)

    print_opCode(deploy_list)
    print_opCode(contract_list)

    print(bzzr+"\n\n")
    print(augs)


