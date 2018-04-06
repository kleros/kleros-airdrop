from web3.auto import w3
from eth_keys import keys

# NOTE tx signing is being audited. safe enough for local signing
w3.eth.enable_unaudited_features()

def sign_tx(tx_dict, key):
    raw_key = bytearray.fromhex(key)
    signed = w3.eth.account.signTransaction(tx_dict, raw_key)

    return signed

def get_address_from_key(key):
    raw_key = bytearray.fromhex(key)
    pk = keys.PrivateKey(raw_key)
    pub_key = keys.PublicKey.from_private(pk)

    return pub_key.to_checksum_address()
