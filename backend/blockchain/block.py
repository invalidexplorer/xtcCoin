import time
from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.util.hex_to_binary import hex_to_binary

GENSIS_DATA = {
    'timestamp':1,
    'last_hash':'gensis_last_hash',
    'hash':'gensis_hash',
    'data':[],
    'difficulty': 3,
    'nonce': 'genesis_nonce',
}
#global variable
class Block:
    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data,
        until a block hash is found that meets the leading 0's requirment.
        """
        timestamp = time.time()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulity(last_block,timestamp)
        nonce = 0
        hash = crypto_hash(timestamp,last_hash,data, difficulty, nonce)
        
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce +=1
            timestamp = time.time()
            difficulty = Block.adjust_difficulity(last_block,timestamp)
            hash = crypto_hash(timestamp,last_hash,data, difficulty, nonce)
            
        return Block(timestamp,last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Generate the gensis block.
        """
        
        # return Block(
        # GENSIS_DATA['timestamp'],
        # GENSIS_DATA['last_hash'],
        # GENSIS_DATA['hash'],
        # GENSIS_DATA['data'],
        # GENSIS_DATA['difficulty'],
        # GENSIS_DATA['nonce'],
        # )
        return Block(**GENSIS_DATA)

        """
        block: a unit of storage
        stores transaction in a blockchain that supports a cryptocurrency
        """
    @staticmethod   
    def from_json(block_json):
        """
        json -> block
        """
        return Block(**block_json)
    
    @staticmethod
    def is_valid_block(last_block, block):
        """
        matches the last hash, 
        verfies the current hash
        checks if the difficulty has been shifted by more than 1
        verfies the work of proof
        """
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')
        if hex_to_binary(block.hash)[0:block.difficulty] != '0'* block.difficulty:
            raise Exception('The proof of work was not right')
        if abs(last_block.difficulty - block.difficulty)>1:
            raise Exception('The block difficulty must only be adjusted by 1')
        
        rehash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )
        
        if block.hash != rehash:
            raise Exception('The block hash must be correct')
            
    @staticmethod
    def adjust_difficulity(last_block, new_timestamp):
        """
        adjust the difficulty to make sure that the mining rate is maintained
        decr the difficulty for slow current mine rate
        incr the difficulty for fast current mine rate
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
            
        if (last_block.difficulty-1)>0:
            return last_block.difficulty -1
        
        return 1
    

    def to_json(self):
        """
        Serialize the block into a dict of its attributes
        """
        return self.__dict__
        
    def __init__(self,timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce
        
    def __repr__(self):
        return (
            'Block('
            f'Timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce}) '
            )
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(Block.genesis(), 'foo')
    #bad_block.last_hash = 'bad_data'
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')
        
    block = Block.mine_block(genesis_block, 'foo')
    print(block)
    
if __name__ == '__main__':
    main()