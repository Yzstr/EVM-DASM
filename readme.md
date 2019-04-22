# EVM-DASM
Convert EVM Bytecode to Opcode refer to the [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf).

## Example

A fregment of BNB's Bytecode from [Etherscan](https://etherscan.io/address/0xB8c77482e45F1F44dE1745F52C74426C631bDD52#code).

``` bash
python EVM-DASM.py
Bytecode(hex):606060405234156200001057
```

```
PUSH1 60
PUSH1 40
MSTORE
CALLVALUE
ISZERO
PUSH3 000010
JUMPI
```

## TODO
- Add expections
- Retrieve stack status

## License
MIT