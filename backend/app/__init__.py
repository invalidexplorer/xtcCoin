from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import  Wallet
from backend.wallet.transaction import  Transaction
from backend.wallet.transaction_pool import  TransactionPool
import os
import requests
import random
app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)
@app.route('/')
def default():
    return 'Blockchain 2.0v'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    #'Stubbed_transaction_data'
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transaction(blockchain)
    return jsonify(block.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})
    

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    # {'recipient' : 'foo', 'amount' : 15}
    transaction_data = request.get_json()
    transaction = transaction_pool.exisiting_transaction(wallet.address)
    
    if transaction:
        transaction.update(wallet,
                              transaction_data['recipient'],
                              transaction_data['amount']
                )
    else:
        transaction = Transaction(wallet,
                                transaction_data['recipient'],
                                transaction_data['amount']
                                )
        
    
    
    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())


ROOT_PORT = 5000
PORT = 5000

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001,6000)
    """
    Peer starts
    """
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    #print(f'result: {result.json}')
    
    result_blockchain = Blockchain.from_json(result.json())
    
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- Successfully synched the chain')
    except Exception as e:
        print(f'\n -- Error Synch')
        
        
app.run(port=PORT)

