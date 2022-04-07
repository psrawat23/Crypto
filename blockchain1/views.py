from http.client import HTTPResponse
from lib2to3.pgen2 import parse
from pydoc import resolve
from urllib import request, response
from uuid import uuid4
from django.shortcuts import render
import datetime
import hashlib
import json
from django.http import JsonResponse
from urllib.parse import urlparse
import requests
from django.http import HttpResponse
def index(request):
    return render(request,"index.html")

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions=[]
        self.nodes=set()
        self.create_block(nonce = 1, previous_hash = '0')


    def create_block(self, nonce, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash,
                 'transactions':self.transactions }
        self.transactions=[]
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transactions(self,sender,reciever,amount):
        self.transactions.append({'sender':sender,'reciever':reciever,'amount':amount})
        previous_block=self.get_previous_block()
        return previous_block['index']+1

    def add_node(self,address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network= self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for node in network:
            response=requests.get(f'http://{node}/get_chain')
            if response.status_code==200:
                length=response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length=length
                    longest_chain=chain
        if longest_chain:
            self.chain=longest_chain
            return True
        return False
        
                
#creating an address for the node on Port 5000

node_address=str(uuid4()).replace('-','')

# Creating our Blockchain
blockchain = Blockchain()

# Mining a new block
def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        blockchain.add_transactions(sender=node_address,reciever="Purushottam",amount=1)
        block = blockchain.create_block(nonce, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash'],
                    'transactions':block['transactions']
                    }
    return JsonResponse(response)


def add_transaction(request):
    json=request.get_json()
    transaction_key=['sender','reciever','amount']
    if not all (key for key in transaction_key):
        return HttpResponse("Some element of the transactions are misssing" ,status=400)
    index=blockchain.add_transactions(json['sender'],json['reciever'],json['amount'])
    response={'message':f'This transaction will be added to Block{index}'}
    return JsonResponse(response)

#part3 Decentralizing our Blockchain


#Connecting new nodes
def connect_node(request):
    json=request.get_json()
    json.get('node')
    

# Getting the full Blockchain
def get_chain(request):
    if request.method == 'GET':
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return JsonResponse(response)

# Checking if the Blockchain is valid
def is_valid(request):
    if request.method == 'GET':
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return JsonResponse(response)