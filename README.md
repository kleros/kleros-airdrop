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
Note: Only need to include twitter and telegram credentials if you are generating `airdrop.csv` via a script.

- Create a `.csv` in the format `address,amount`
e.g.
```
0x1234....,1000000
```

Alternatively you can use `generate_airdrop_csv.py` to generate this CSV. This script pulls telegram and
twitter followers and cross references them against the subscriber csv from the signup form.

- Run airdropping script
```
python airdrop.py <your_file>.csv
```

## Generate Airdrop CSV

#### Usage:

- Ensure that you have created twitter and telegram api access tokens and input your credentials into
`config.py`. NOTE: The credentialed telegram account must be an admin to access the user data.

- To pull followers via the api:
```
python generate_airdrop_csv.py --subscribers <subscriber_file>.csv
```

Note: There are hardcoded indicies that correspond to Kleros' subscriber csv. Change these in the script
for other usage.

This will generate a `.csv` of the usernames pulled from each platform respectively. They can be passed
as named arguments for subsequent use.

- To generate `airdrop.csv` with pre-existing follower .csv's
```
python generate_airdrop_csv.py --subscribers <subscriber_file>.csv --twitter <twitter_handles>.csv --telegram <telegram_usernames>.csv
```

## Notes:
- The private key you use must be the same private key that deployed the Airdropper.sol smart contract.
- ERC20 contract should give value to the `Airdropper` contract before this is run.
