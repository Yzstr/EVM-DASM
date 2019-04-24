# EVM-DASM
Convert EVM Bytecode to Opcode refer to the [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf).

# Usage
The input opcode must include the deployment opcode rather than just contract opcode. A valid input may follow the pattern as follows.

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

Bytecodes from Etherscan is applicable, feel free to copy all the bytecodes of a contract and take it as input of the script.


## Example

All the bytecodes of BNB's from [Etherscan](https://etherscan.io/address/0xB8c77482e45F1F44dE1745F52C74426C631bDD52#code) were copied into bnb.bin and the output is clear.

``` bash
cat bnb.bin | python3 EVM-DASM.py > bnb.txt
```

```
Bytecode(hex):


**********************************************************************
Deployment Opcode
**********************************************************************
11608
60: PUSH1 60
60: PUSH1 40
52: MSTORE
34: CALLVALUE
15: ISZERO

·
·
·

62: PUSH3 0001ed
60: PUSH1 00
39: CODECOPY
60: PUSH1 00
f3: RETURN
00: STOP



**********************************************************************
Contract Opcode Below
**********************************************************************
60: PUSH1 60
60: PUSH1 40
52: MSTORE
36: CALLDATASIZE
15: ISZERO
61: PUSH2 00d9
57: JUMPI
60: PUSH1 00

·
·
·

fd: REVERT
5b: JUMPDEST
5b: JUMPDEST
50: POP
56: JUMP
00: STOP
11608



**********************************************************************
What's this? ("00" is trivial)
**********************************************************************
00




**********************************************************************
bzzr code
**********************************************************************
bzzr: 082734e053ffbdf2a3195354a3210dff3723c239a1e76ae3be0936f6aed31bee



**********************************************************************
ABI Augs
**********************************************************************
Arg [1]: 000000000000000000000000000000000000000000a56fa5b99019a5c8000000
Arg [2]: 0000000000000000000000000000000000000000000000000000000000000080
Arg [3]: 0000000000000000000000000000000000000000000000000000000000000012
Arg [4]: 00000000000000000000000000000000000000000000000000000000000000c0
Arg [5]: 0000000000000000000000000000000000000000000000000000000000000003
Arg [6]: 424e420000000000000000000000000000000000000000000000000000000000
Arg [7]: 0000000000000000000000000000000000000000000000000000000000000003
Arg [8]: 424e420000000000000000000000000000000000000000000000000000000000

```

## TODO
- Add expections
- Retrieve stack status

## License
MIT