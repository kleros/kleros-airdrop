import sys
import csv
import json

from web3 import Web3, HTTPProvider
from config import config
from tools.txs import sign_tx, get_address_from_key

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise RuntimeError('Missing required parameter: path/to/airdrop.csv')
    # csv for airdrop
    airdrop_csv = sys.argv[1]
    # size of each tx batch
    batch_size = config['BATCH_SIZE']
    # web3
    HTTPProvider = HTTPProvider(config['ETH_PROVIDER'])
    w3 = Web3(HTTPProvider)
    # contract
    airdropper_json = open(file='contracts/Airdropper.json')
    abi = json.loads(airdropper_json.read())['abi']
    airdropper = w3.eth.contract(address=config['AIRDROPPER_CONTRACT_ADDRESS'], abi=abi)
    # keys
    pk = config['PRIVATE_KEY']
    address = get_address_from_key(pk)
    # starting nonce
    nonce = w3.eth.getTransactionCount(address)

    recipient_batch = []
    value_batch = []
    # airdrop fn
    def airdrop_batch(recipients, values):
        airdrop_tx = airdropper.functions.airdropTokens(
            recipients,
            values
        ).buildTransaction({
            'gas': config['GAS'],
            'gas_price': w3.toWei('1', 'gwei'),
            'nonce': nonce,
        })

        signed_tx = sign_tx(airdrop_tx, pk)
        w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_hash = w3.toHex(w3.sha3(signed_tx.rawTransaction))
        print('tx hash for batch: %s' % tx_hash)

    with open(airdrop_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            recipient_batch.append(row[0])
            value_batch.append(int(row[1]))

            if (len(recipient_batch) == batch_size):
                airdrop_batch(recipient_batch, value_batch)
                # reset batch
                recipient_batch = []
                value_batch = []
                nonce += 1

        # airdrop all the left overs
        airdrop_batch(recipient_batch, value_batch)
