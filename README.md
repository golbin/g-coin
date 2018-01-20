# G Coin

A simple implementation of Blockchain for understanding easily.

It includes only basic concepts.

- Block and Hash
- Transaction and Balance
- Mining with Proof of Work
- Chain validation and consensus conflicts

## Modules

**bold** is core function.

- blockchain : chain structure /w blocks
    - **new_block**: make block /w hash of previous block and current proof
    - **valid**: validate chain rules of all chain
- block : block structure
    - **hash**: hash itself
- proof : proof of work
    - **find_proof**
    - **valid_proof**
- transaction : data object
- book : book of transactions
    - **check_balance** /w transaction history of sender account
- node
    - **consensus_with_neighbor**

## Endpoints

- `/transaction` : Add a transaction and get pending transactions.
- `/mine` : Mining. Find proof and make block with rewards.
- `/node` : Add a node as a neighbor node
- `/chain` : Get full chain to validate.
- `/chain/valid` : Valid chain
- `/chain/consensus` : Consensus conflicts

### Try using Insomnia

- Download [Insomnia](https://insomnia.rest/)
- Import from insomnia.json

![](images/transaction.png)
![](images/mining.png)

### Try like this

- First try
    - POST `/transaction`
        - /w {sender: '0', recipient: 'golbin', amount: 10}
    - GET `/transaction`
    - GET `/chain`
    - POST `/mine`
    - GET `/chain`
    - GET `/transaction`
- Second try
    - POST `/transaction`
        - /w {sender: 'golbin', recipient: 'bluecat', amount: 10}
    - POST `/transaction`
        - /w {sender: 'golbin', recipient: 'bluecat', amount: 10}
    - POST `/mine`
    - GET `/chain`

### Try endpoints to run two daemons.

```bash
python app.py --port 5000
python app.py --port 5001
```

- POST `/node`
    - to 127.0.0.1:5000 /w {address: '127.0.0.1:5001'}
- POST `/node`
    - to 127.0.0.1: 5001 /w {address: '127.0.0.1:5000'}
- Try several mining
- GET `/chain/valid`
- POST `/chain/consensus`

## Requirements

- Python >= 3.6
- Flask >= 0.12
- Requests >= 2.18

## References

- http://ecomunsing.com/build-your-own-blockchain
- https://qiita.com/hidehiro98/items/841ece65d896aeaa8a2a
