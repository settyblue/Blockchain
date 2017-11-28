import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain.
        """

        :param proof: <int> The proof given by the Proof-of-Work Algorithm
        :param previous_hash: (Optional) <str> Hash of the previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions.
        """
        Creates a new transaction to go into the next mined block

        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of he Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction.
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a Block
        """
        Creates a SHA-256 hash of a Block

        :param block: <dict> Block
        :return: <str>
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates he proof: Does hash(last_proof, proof) contain leading 4 zeros?
        :param last_proof:
        :param proof:
        :return:
        """

        guess = f'{last_proof*proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
