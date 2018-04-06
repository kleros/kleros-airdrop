# Airdropper

Airdropper smart contract and tools to airdrop tokens read from a .csv

Requires `python 3.5+`

Recommended to use a virtualenv:
- Install a virtualenv
```
virtualenv --python=/path/to/your/python3 .venv  
```
- Acivate env
```
source .venv/bin/activate  
```

## Quickstart:
- Install requirements
```
pip install -r requirements.txt
```

- Create a `config.py` file in the root. See `example.config.py`.

- Create a `.csv` in the format `address,amount`
e.g.
```
"0x1234....",1000000
```

- Run script
```
python airdrop.py <youfile>.csv
```

## Notes:
- The private key you use must be the same private key that deployed the Airdropper.sol smart contract.
- ERC20 contract should give value to the `Airdropper` contract before this is run.
