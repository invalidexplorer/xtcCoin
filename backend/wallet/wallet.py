import uuid
from backend.config import  STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.exceptions import InvalidSignature


import json
class Wallet:
    """
    An indv wallet for a miner
    Keeps track of transaction
    allows auth
    """
    
    def __init__(self, blockchain = None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        #self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.seriallize_public_key()
        
    @property #code runes everytime balance is accessed
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)
        

    
    def sign(self, data):
        """
        Genereated a signature based on the data using the local private key
        """
        return decode_dss_signature(self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256())))
    
    def seriallize_public_key(self):
        """
        instance - > jsonizable data
        """
        self.public_key_bytes = self.public_key.public_bytes(encoding=serialization.Encoding.PEM
                                                             ,format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        
    
        self.public_key = self.public_key_bytes
        
        
        
    @staticmethod
    def verfiy(public_key, data, signature):
        """
        verfies a signature
        """
        deserialized_public_key = serialization.load_pem_public_key(public_key.encode('utf-8'),
                                                                    default_backend())
        
        (r,s) = signature
        try:
            deserialized_public_key.verify(encode_dss_signature(r,s), 
                            json.dumps(data).encode('utf-8'),
                            ec.ECDSA(hashes.SHA256())
                            )
            return True
        except InvalidSignature:
            return False
        
    @staticmethod
    def calculate_balance(blockchain, address):
        """
        calcualte the balance of the given address considerng the transaction data in the blockchain.
        
        The balance is found by adding the output values that belong to the address
        since the most recent transaction by that address
        """
        balance = STARTING_BALANCE

        if not blockchain:
            return balance
        
        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    "Any time the address conducts a new transaction it resets balance"
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]
        return balance
    
                        
            
            
                
    
def main():
    wallet = Wallet()
    print(f'wallet.__dict__:{wallet.__dict__}')
    data = {'foo':'bar'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')
    should_be_valid = Wallet.verfiy(wallet.public_key, data, signature)
    print(f'should_be_valid: {should_be_valid}')
    
    should_be_invalid = Wallet.verfiy(Wallet().public_key, data, signature)
    print(f'Should_be_invalid: {should_be_invalid}')

if __name__ == '__main__':
    main()
    
        
        