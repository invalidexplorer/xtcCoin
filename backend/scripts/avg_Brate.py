from backend.blockchain.blockchain import Blockchain
from time import time
blockchain = Blockchain()
times = []

for i in range(1000):
    start_time = time()
    blockchain.add_block(i)
    end_time = time()
    
    time_to_mine = end_time - start_time
    times.append(time_to_mine)

    avgtime = sum(times)/len(times)
    print(f'New block difficulty: {blockchain.chain[-1].difficulty}')
    print(f'New block time: {time_to_mine} ')
    print(f'New block avg time: {avgtime} \n ')
    