from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import  MINING_REWARD_INPUT, MINING_REWARD
from backend.wallet.wallet import Wallet 
class Blockchain:
    """
    Blockchain: public ledger of transactions
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]
        
    def add_block(self, data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))  
    
    def __repr__(self):
        return f'Blockchain:{self.chain}'
    
    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized block into a blockchain
        the result will contain a chain list of block
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
        return blockchain
    def replace_chain(self,chain):
        """
        Replace the local chain iff
        1. New chain is longer than the local chain
        2. New chain is formatted correctly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer')
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid')
        
        self.chain = chain
    
    
    def to_json(self):
        """
        serialize the chain
        """
        return list(map(lambda block: block.to_json(), self.chain))
    
    @staticmethod
    def is_valid_chain(chain):
        """
        validate the incoming chain
        enforce the following rules of the blockvhain
        -the chain must start with the gensis block
        -block must be formatted correctly 
        """
        if chain[0] != Block.genesis():
            raise Exception('The gensis block must be valid')
            
        for i in range(1,len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block,block)
        
        Blockchain.is_valid_chain(chain)
            
    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        enforces the rules of a chain composed of blocks of transctions.
         - Each transaction must only appear once in a chain
         - there can only be one mining reward per block
         - each transaction must be valid
         
        """
        transaction_ids = set()
        
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            
            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)
                
                
                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is duplicated')
                
                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception('Invalid mining rewards'\
                            f'check with the hash: {block.hash}')
                    has_mining_reward = True               
                
                else:
                    transaction_ids.add(transaction.id)
                    
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain, transaction.input['address']
                    )
                    
                    if historic_balance != transaction.input['amount']:
                        raise Exception(
                            f'Transaction {transaction.id} has an invalid input amount'
                        )
                    
                Transaction.is_valid_transaction(transaction)
                        
            
        
def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)

if __name__=='__main__':
    main()
#this is used for running the debuging code
#when a .py file is imported as a module, the 
#first function that runs is by the name of the file, not main
#main only runs when the file is directly started as a script

    
        