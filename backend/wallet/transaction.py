import uuid
import time

from backend.wallet.wallet import  Wallet
from backend.config import  MINING_REWARD, MINING_REWARD_INPUT
class Transaction:
    """
    Documents an exchange from a sender to one or more recievers
    """
    def __init__(self, sender_wallet = None, recipient = None, amount = None, id = None, output = None, input = None):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)
    
    def create_output(self, sender_wallet, recipient, amount):
        
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')
        output ={}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount
        
        return output
    
    def create_input(self, sender_wallet, output):
        """
        Structure the input data for the transaction
        Sign the transaction and include the sender's PK & address
        """
        return {
            'timestamp' : time.time(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        } 
        
    def update(self, sender_wallet, recipient, amount):
        """
        Update the transaction with an existing or new recipient
        """  
        if amount > self.output[sender_wallet.address]:
            raise  Exception('Amount exceeds balance')
        
        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount
        
        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount
        
        self.input = self.create_input(sender_wallet, self.output)
    
    def to_json(self):
        """
        Serialize the transaction
        """
        return self.__dict__
    
    @staticmethod
    def from_json(transaction_json):
        """
        Deseriallize a trnasaction's json representation back into Transaction instance
        """
        
        return Transaction(**transaction_json)
        
        
    
    @staticmethod
    def is_valid_transaction(transaction):
        """
        Validate a transaction
        raise an exception for invalid transaction 
        """
        if transaction.input == MINING_REWARD_INPUT:
           if list(transaction.output.values()) != MINING_REWARD:
               raise Exception('Invalid mining reward')
           return
           
           
        output_total = sum(transaction.output.values())
        
        if transaction.input['amount']!= output_total:
            raise Exception('Invalid transaction output values')
        
        if not Wallet.verfiy(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']  
        ):
            raise  Exception('Invalid Signature')
        
    @staticmethod
    def reward_transaction(miner_wallet):
        """
        Generate a reward transaction that award the miner
        """
        output = {}
        output[miner_wallet.address] = MINING_REWARD
        
        return Transaction(input=MINING_REWARD_INPUT, output=output)
    
def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__: {transaction.__dict__}')
    
    transaction_json = transaction.to_json()
    restored_transaction = Transaction.from_json(transaction_json)
    
    print(f'Restored_trasnaction.__dict__: {restored_transaction}')

if __name__ == '__main__':
    main()
    