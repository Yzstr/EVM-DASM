import json
import sha3

function_name=[]

with open('bnb.abi','r') as f:
    data=json.load(f)
# print(data)
for dict in data:
    if dict["type"]=="function":
        # print(dict["name"])
        name=dict["name"]
        name+='('
        if not dict['inputs']:
            name+=')'
        else:
            for sub_dict in dict['inputs']:
                name+=sub_dict['type']
                name+=','  
            name=name[:-1]
            name+=')'          
        
        function_name.append(name)

print(function_name)

function_name_hash=dict.fromkeys(function_name)
for name in function_name_hash.keys():
    function_name_hash[name]=sha3.keccak_256(name.encode('utf-8')).hexdigest().upper()[:8]

print(function_name_hash)
