class TransactionPool:
    def __init__(self):
        self.transaction_map={}
    
    def set_transaction(self, transaction):
        """
        set a transaction in the transaction pool
        """
        self.transaction_map[transaction.id] = transaction
        
    def exisiting_transaction(self, address):
        """
        Find a transaction genereated by the address in the transaction
        """
        
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == address:
                return transaction
    
    def transaction_data(self):
        """
        return the transaction the pool data ~ json
        """
        return list(map(lambda transaction: transaction.to_json(), self.transaction_map.values()))
    
    def clear_blockchain_transaction(self, blockchain):
        """
        delete blockchain recorded transaction from the transaction
        """
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except  KeyError:
                    pass
                
        
        