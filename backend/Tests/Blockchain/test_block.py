from backend.blockchain.block import Block, GENSIS_DATA
from time import sleep, time
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary
import pytest

@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block,'Test-data')

def test_mine_block():
    last_block = Block.genesis()
    data = 'Test-data'
    block = Block.mine_block(last_block,data)
    
    assert isinstance(block,Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0'*block.difficulty
    
def test_gensis():
    gensis = Block.genesis()
    assert isinstance(gensis,Block)
   
    for key, value in GENSIS_DATA.items():
        assert getattr(gensis,key) == value
        

def test_slowly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    sleep(MINE_RATE)
    mined_block = Block.mine_block(last_block, 'z1234')
    
    assert last_block.difficulty - mined_block.difficulty == +1
    
def test_quickly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'z1234')
    
    assert last_block.difficulty - mined_block.difficulty == -1
    
def test_mined_difficulty_limits_at_1():
    last_block = Block(time(),'test_last_hash', 'test_hash', 'test_data', 1 ,0)
    sleep(MINE_RATE)
    mined_block = Block.mine_block(last_block, 'bar')
    
    assert mined_block.difficulty == 1 
    
def test_is_valid_block():
    last_block = Block.genesis()
    block = Block.mine_block(last_block,'foo')
    Block.is_valid_block(last_block,block)
    
def test_is_valid_bad_block():
    last_block = Block.genesis()
    block = Block.mine_block(last_block,'foo')
    block.last_hash = 'evil_lash_harsh'
    
    with pytest.raises(Exception, match = 'he block last_hash must be correct'):
        Block.is_valid_block(last_block, block)

def test_is_valid_bad_proof_of_work(last_block, block):
    block.hash = 'fff'
    
    with pytest.raises(Exception, match='The proof of work was not right'):
        Block.is_valid_block(last_block,block)

def test_is_valid_jumped_difficulty(last_block, block):
    jd = 10
    block.difficulty = jd
    block.hash = f'{"0"*jd}111abc'
    with pytest.raises(Exception, match='The block difficulty must only be adjusted by 1'):
        Block.is_valid_block(last_block,block)

def test_is_valid_block_bad_hash(last_block, block):
    block.hash = '000000000000000000000adad'
    
    with pytest.raises(Exception, match='The block hash must be correct'):
        Block.is_valid_block(last_block, block)
    