# EVM-DASM
Convert EVM byteCode to opCode via the [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf).

# Usage

``` bash
    python3 EVM-DASM.py contract.bin contract.abi
```

Note that the input `contract.bin` shall contain the deployment byteCode rather than contract byteCode only. A valid input may has the pattern below.


```
+-------------------+-------------------------------------------------------------------+
| Part              | Notes                                                             |
+-------------------+-------------------------------------------------------------------+
| Deployment Opcode | The instructions that tell EVM how to deploy the contract opcode. |
+-------------------+-------------------------------------------------------------------+
| Contract Opcode   |                                                                   |
+-------------------+-------------------------------------------------------------------+
| ?                 | Some contracts has unknown part in this position.                 |
+-------------------+-------------------------------------------------------------------+
| bzzr code         | The address that indicates swarm source.                          |
+-------------------+-------------------------------------------------------------------+
| ABI Augs          | ABI list                                                          |
+-------------------+-------------------------------------------------------------------+
```

Feel free to copy the byteCodes of a conratct from Etherscan which already contains deployment byteCodes. If you want to parse a byteCode file without deployment byteCode at the begining, set the value of `isDeploy` to `False` in the function `split_byteCode()`.

The abi of a contract `contract.abi` is needed for function analysis. And you may need to install SHA-3 wrapper(keccak) for Python.

``` bash
    pip install pysha3
```



## Example

Bytecodes of BNB from [Etherscan](https://etherscan.io/address/0xB8c77482e45F1F44dE1745F52C74426C631bDD52#code) and abi of BNB are inputs.

``` bash
    python3 EVM-DAMS.py bnb.bin bnb.abi > bnb.txt
```

First, we got the abi hash table first, which provides function name and function hash.

```
{'06fdde03': ['name()', ''],
 '095ea7b3': ['approve(address,uint256)', ''],
 '18160ddd': ['totalSupply()', ''],
 '23b872dd': ['transferFrom(address,address,uint256)', ''],
 '313ce567': ['decimals()', ''],
 '3bed33ce': ['withdrawEther(uint256)', ''],
 '42966c68': ['burn(uint256)', ''],
 '6623fc46': ['unfreeze(uint256)', ''],
 '70a08231': ['balanceOf(address)', ''],
 '8da5cb5b': ['owner()', ''],
 '95d89b41': ['symbol()', ''],
 'a9059cbb': ['transfer(address,uint256)', ''],
 'cd4217c1': ['freezeOf(address)', ''],
 'd7a78db8': ['freeze(uint256)', ''],
 'dd62ed3e': ['allowance(address,address)', '']}
```

Second, we got the deployment opCode.

```
0x00000000:  60   PUSH1       60
0x00000002:  60   PUSH1       40
0x00000004:  52   MSTORE       
0x00000005:  34   CALLVALUE       
0x00000006:  15   ISZERO       
0x00000007:  62   PUSH3       000010
0x0000000b:  57   JUMPI       
0x0000000c:  60   PUSH1       00
0x0000000e:  80   DUP1       
0x0000000f:  fd   REVERT       
.
.
.
0x000001dd:  5b   JUMPDEST       
0x000001de:  61   PUSH2       14eb
0x000001e1:  80   DUP1       
0x000001e2:  62   PUSH3       0001ed
0x000001e6:  60   PUSH1       00
0x000001e8:  39   CODECOPY       
0x000001e9:  60   PUSH1       00
0x000001eb:  f3   RETURN       
0x000001ec:  00   STOP   
```

Third, we got the contract opCode. Note that the Function Head appears in the top of contract opCode.

```
0x00000000:  60   PUSH1       60
0x00000002:  60   PUSH1       40
0x00000004:  52   MSTORE       
0x00000005:  36   CALLDATASIZE       
0x00000006:  15   ISZERO       
0x00000007:  61   PUSH2       00d9
0x0000000a:  57   JUMPI       
0x0000000b:  60   PUSH1       00
0x0000000d:  35   CALLDATALOAD       
0x0000000e:  7c   PUSH29       0100000000000000000000000000000000000000000000000000000000
0x0000002c:  90   SWAP1       
0x0000002d:  04   DIV       
0x0000002e:  63   PUSH4       ffffffff
0x00000033:  16   AND       

Function Head:   name()
0x00000034:  80   DUP1       
0x00000035:  63   PUSH4       06fdde03
0x0000003a:  14   EQ       
0x0000003b:  61   PUSH2       00e2
0x0000003e:  57   JUMPI       

Function Head:   approve(address,uint256)
0x0000003f:  80   DUP1       
0x00000040:  63   PUSH4       095ea7b3
0x00000045:  14   EQ       
0x00000046:  61   PUSH2       0171
0x00000049:  57   JUMPI       
.
.
.
Function Head:   freeze(uint256)
0x000000c3:  80   DUP1       
0x000000c4:  63   PUSH4       d7a78db8
0x000000c9:  14   EQ       
0x000000ca:  61   PUSH2       04f5
0x000000cd:  57   JUMPI       

Function Head:   allowance(address,address)
0x000000ce:  80   DUP1       
0x000000cf:  63   PUSH4       dd62ed3e
0x000000d4:  14   EQ       
0x000000d5:  61   PUSH2       0530
0x000000d8:  57   JUMPI

0x000000d9:  5b   JUMPDEST       
0x000000da:  61   PUSH2       00e0
0x000000dd:  5b   JUMPDEST       
0x000000de:  5b   JUMPDEST       
0x000000df:  56   JUMP       
0x000000e0:  5b   JUMPDEST       
0x000000e1:  00   STOP       
```

The Function Head has indicated the address of the Function Body in `PUSH2` operation, thus we can find all the Function Bodies in the contract.

```
Function Body:   name()
0x000000e2:  5b   JUMPDEST       
0x000000e3:  34   CALLVALUE       
0x000000e4:  15   ISZERO       
0x000000e5:  61   PUSH2       00ed
0x000000e8:  57   JUMPI       
0x000000e9:  60   PUSH1       00
0x000000eb:  80   DUP1       
0x000000ec:  fd   REVERT       
0x000000ed:  5b   JUMPDEST       
0x000000ee:  61   PUSH2       00f5
0x000000f1:  61   PUSH2       059c
0x000000f4:  56   JUMP       
0x000000f5:  5b   JUMPDEST       
0x000000f6:  60   PUSH1       40
0x000000f8:  51   MLOAD       
0x000000f9:  80   DUP1       
0x000000fa:  80   DUP1       
0x000000fb:  60   PUSH1       20
0x000000fd:  01   ADD       
0x000000fe:  82   DUP3       
0x000000ff:  81   DUP2       
0x00000100:  03   SUB       
0x00000101:  82   DUP3       
0x00000102:  52   MSTORE       
0x00000103:  83   DUP4       
0x00000104:  81   DUP2       
0x00000105:  81   DUP2       
0x00000106:  51   MLOAD       
0x00000107:  81   DUP2       
0x00000108:  52   MSTORE       
0x00000109:  60   PUSH1       20
0x0000010b:  01   ADD       
0x0000010c:  91   SWAP2       
0x0000010d:  50   POP       
0x0000010e:  80   DUP1       
0x0000010f:  51   MLOAD       
0x00000110:  90   SWAP1       
0x00000111:  60   PUSH1       20
0x00000113:  01   ADD       
0x00000114:  90   SWAP1       
0x00000115:  80   DUP1       
0x00000116:  83   DUP4       
0x00000117:  83   DUP4       
0x00000118:  60   PUSH1       00
0x0000011a:  5b   JUMPDEST       
0x0000011b:  83   DUP4       
0x0000011c:  81   DUP2       
0x0000011d:  10   LT       
0x0000011e:  15   ISZERO       
0x0000011f:  61   PUSH2       0136
0x00000122:  57   JUMPI       
0x00000123:  80   DUP1       
0x00000124:  82   DUP3       
0x00000125:  01   ADD       
0x00000126:  51   MLOAD       
0x00000127:  81   DUP2       
0x00000128:  84   DUP5       
0x00000129:  01   ADD       
0x0000012a:  52   MSTORE       
0x0000012b:  5b   JUMPDEST       
0x0000012c:  60   PUSH1       20
0x0000012e:  81   DUP2       
0x0000012f:  01   ADD       
0x00000130:  90   SWAP1       
0x00000131:  50   POP       
0x00000132:  61   PUSH2       011a
0x00000135:  56   JUMP       
0x00000136:  5b   JUMPDEST       
0x00000137:  50   POP       
0x00000138:  50   POP       
0x00000139:  50   POP       
0x0000013a:  50   POP       
0x0000013b:  90   SWAP1       
0x0000013c:  50   POP       
0x0000013d:  90   SWAP1       
0x0000013e:  81   DUP2       
0x0000013f:  01   ADD       
0x00000140:  90   SWAP1       
0x00000141:  60   PUSH1       1f
0x00000143:  16   AND       
0x00000144:  80   DUP1       
0x00000145:  15   ISZERO       
0x00000146:  61   PUSH2       0163
0x00000149:  57   JUMPI       
0x0000014a:  80   DUP1       
0x0000014b:  82   DUP3       
0x0000014c:  03   SUB       
0x0000014d:  80   DUP1       
0x0000014e:  51   MLOAD       
0x0000014f:  60   PUSH1       01
0x00000151:  83   DUP4       
0x00000152:  60   PUSH1       20
0x00000154:  03   SUB       
0x00000155:  61   PUSH2       0100
0x00000158:  0a   EXP       
0x00000159:  03   SUB       
0x0000015a:  19   NOT       
0x0000015b:  16   AND       
0x0000015c:  81   DUP2       
0x0000015d:  52   MSTORE       
0x0000015e:  60   PUSH1       20
0x00000160:  01   ADD       
0x00000161:  91   SWAP2       
0x00000162:  50   POP       
0x00000163:  5b   JUMPDEST       
0x00000164:  50   POP       
0x00000165:  92   SWAP3       
0x00000166:  50   POP       
0x00000167:  50   POP       
0x00000168:  50   POP       
0x00000169:  60   PUSH1       40
0x0000016b:  51   MLOAD       
0x0000016c:  80   DUP1       
0x0000016d:  91   SWAP2       
0x0000016e:  03   SUB       
0x0000016f:  90   SWAP1       
0x00000170:  f3   RETURN       
·
·
·
Function Body:   allowance(address,address)
0x00000530:  5b   JUMPDEST       
0x00000531:  34   CALLVALUE       
0x00000532:  15   ISZERO       
0x00000533:  61   PUSH2       053b
0x00000536:  57   JUMPI       
0x00000537:  60   PUSH1       00
0x00000539:  80   DUP1       
0x0000053a:  fd   REVERT       
0x0000053b:  5b   JUMPDEST       
0x0000053c:  61   PUSH2       0586
0x0000053f:  60   PUSH1       04
0x00000541:  80   DUP1       
0x00000542:  80   DUP1       
0x00000543:  35   CALLDATALOAD       
0x00000544:  73   PUSH20       ffffffffffffffffffffffffffffffffffffffff
0x00000559:  16   AND       
0x0000055a:  90   SWAP1       
0x0000055b:  60   PUSH1       20
0x0000055d:  01   ADD       
0x0000055e:  90   SWAP1       
0x0000055f:  91   SWAP2       
0x00000560:  90   SWAP1       
0x00000561:  80   DUP1       
0x00000562:  35   CALLDATALOAD       
0x00000563:  73   PUSH20       ffffffffffffffffffffffffffffffffffffffff
0x00000578:  16   AND       
0x00000579:  90   SWAP1       
0x0000057a:  60   PUSH1       20
0x0000057c:  01   ADD       
0x0000057d:  90   SWAP1       
0x0000057e:  91   SWAP2       
0x0000057f:  90   SWAP1       
0x00000580:  50   POP       
0x00000581:  50   POP       
0x00000582:  61   PUSH2       1445
0x00000585:  56   JUMP       
0x00000586:  5b   JUMPDEST       
0x00000587:  60   PUSH1       40
0x00000589:  51   MLOAD       
0x0000058a:  80   DUP1       
0x0000058b:  82   DUP3       
0x0000058c:  81   DUP2       
0x0000058d:  52   MSTORE       
0x0000058e:  60   PUSH1       20
0x00000590:  01   ADD       
0x00000591:  91   SWAP2       
0x00000592:  50   POP       
0x00000593:  50   POP       
0x00000594:  60   PUSH1       40
0x00000596:  51   MLOAD       
0x00000597:  80   DUP1       
0x00000598:  91   SWAP2       
0x00000599:  03   SUB       
0x0000059a:  90   SWAP1       
0x0000059b:  f3   RETURN     
```

The rest of the opCodes needs a further insight. After that is a reconsrtucted abi hash table, which contains the address of each function.

```
{'06fdde03': ['name()', '00e2'],
 '095ea7b3': ['approve(address,uint256)', '0171'],
 '18160ddd': ['totalSupply()', '01cb'],
 '23b872dd': ['transferFrom(address,address,uint256)', '01f4'],
 '313ce567': ['decimals()', '026d'],
 '3bed33ce': ['withdrawEther(uint256)', '029c'],
 '42966c68': ['burn(uint256)', '02bf'],
 '6623fc46': ['unfreeze(uint256)', '02fa'],
 '70a08231': ['balanceOf(address)', '0335'],
 '8da5cb5b': ['owner()', '0382'],
 '95d89b41': ['symbol()', '03d7'],
 'a9059cbb': ['transfer(address,uint256)', '0466'],
 'cd4217c1': ['freezeOf(address)', '04a8'],
 'd7a78db8': ['freeze(uint256)', '04f5'],
 'dd62ed3e': ['allowance(address,address)', '0530']}
 ```

 Then follows the bzzr swarm source of the contract.

```
'bzzr: 082734e053ffbdf2a3195354a3210dff3723c239a1e76ae3be0936f6aed31bee'
```

The last is the Constructor Arguments.

```
['Arg [0]: 000000000000000000000000000000000000000000a56fa5b99019a5c8000000',
 'Arg [1]: 0000000000000000000000000000000000000000000000000000000000000080',
 'Arg [2]: 0000000000000000000000000000000000000000000000000000000000000012',
 'Arg [3]: 00000000000000000000000000000000000000000000000000000000000000c0',
 'Arg [4]: 0000000000000000000000000000000000000000000000000000000000000003',
 'Arg [5]: 424e420000000000000000000000000000000000000000000000000000000000',
 'Arg [6]: 0000000000000000000000000000000000000000000000000000000000000003',
 'Arg [7]: 424e420000000000000000000000000000000000000000000000000000000000']
```



## TODO
- Event analysis
- Add options

## License
MIT