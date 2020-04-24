from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import  SubscribeCallback
from backend.blockchain import block
from backend.blockchain.block import Block
from backend.wallet.transaction import  Transaction
#from backend.wallet.transaction_pool import  TransactionPool
import time
publish_key ='pub-c-d1f30af5-4847-455f-8c88-3a90747dabe6'
subscribe_key = 'sub-c-a8d9dc3c-7b39-11ea-87e8-c6dd1f7701c5'

#transaction_pool = TransactionPool
pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key
CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION' : 'TRANSACTION'
}

class Listner(SubscribeCallback):
    def __init__(self,blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        
    def message(self, pubnub, message_obj):
        print(f'\n--Channel: {message_obj.channel} | Message: {message_obj.message}')
        
        if message_obj.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_obj.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transaction(self.blockchain)
                print('\n -- Successfully replaced the local chain')
            
            except Exception as e:
                print(f'\n -- Didnt replace the chain')
                
        elif message_obj.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_obj.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool')
            
            

class PubSub():
    """
    Handles the publish/subscribe layer of the application
    provides communication btw the nodes of the blockchain method
    """
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listner(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
         """
         Broadcast a block object to all nodes
         """
         self.publish(CHANNELS['BLOCK'],block.to_json())
    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes
        """ 
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())
        
def main():
    pubsub = PubSub()
    
    time.sleep(1)
    
    pubsub.publish(CHANNELS['TEST'],{'foo':'bar'})


if __name__ == '__main__':
    main()
    