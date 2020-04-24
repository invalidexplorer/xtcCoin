import hashlib
import json

def crypto_hash(*args):
    """
    Return a sha-256 hash of the given arguements
    """
    stringfield_args = sorted(map(lambda data: json.dumps(data),args))
    #print(f'stringfield_args:{stringfield_args}')
    joined_data = ''.join(stringfield_args)
    #print(f'joined_data: {joined_data}')
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"Crypto_hash('foo'):{crypto_hash('1',2,3,'4')}")
    
if __name__ == "__main__":
    main()
    