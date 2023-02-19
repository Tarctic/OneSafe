import os
import ipfshttpclient
from database import create_database
import generate_id
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from pymongo import MongoClient
from bson.binary import Binary

from flask import Flask, redirect, request, render_template, session, url_for


app = Flask(__name__)
app.secret_key = "wiehfoiwhelskndf23hohfoish"

@app.route("/")
def index():
    return render_template("index.html")

# Connect to the Goerli test network using Infura
infura_url = "https://goerli.infura.io/v3/ddca8499dc454347a7fa460096535d24"
web3 = Web3(HTTPProvider(infura_url))

address = "0xf5a21117f5e0fF05DdF5C0626f8edDCe1486eE1e"
# connect to a local Ethereum node

# Set the account address and private key for signing transactions
account_address = "0x69c14cc30C634F79A07a3BFed69ff11B095Cb099"
private_key = "ef2896b12a2a55194fcb02c91848483ccd2f1a21b39dc86a536d3aaac87c918c"

# get the contract instance
contract_address = "0xf5a21117f5e0fF05DdF5C0626f8edDCe1486eE1e"
contract_abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "fileId",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "input1",
                "type": "string",
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "input2",
                "type": "string",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "integer1",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "bytes[]",
                "name": "fileInputs",
                "type": "bytes[]",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256",
            },
        ],
        "name": "FilesProcessed",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "input1", "type": "string"},
            {"internalType": "string", "name": "input2", "type": "string"},
            {"internalType": "uint256", "name": "integer1", "type": "uint256"},
            {"internalType": "bytes[]", "name": "fileInputs", "type": "bytes[]"},
        ],
        "name": "processFiles",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "fileRecords",
        "outputs": [
            {"internalType": "string", "name": "input1", "type": "string"},
            {"internalType": "string", "name": "input2", "type": "string"},
            {"internalType": "uint256", "name": "integer1", "type": "uint256"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "input1", "type": "string"},
            {"internalType": "string", "name": "input2", "type": "string"},
            {"internalType": "uint256", "name": "integer1", "type": "uint256"},
            {"internalType": "bytes[]", "name": "fileInputs", "type": "bytes[]"},
        ],
        "name": "generateFilesID",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "input1", "type": "string"},
            {"internalType": "string", "name": "input2", "type": "string"},
            {"internalType": "uint256", "name": "integer1", "type": "uint256"},
        ],
        "name": "generateID",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "fileId", "type": "uint256"}],
        "name": "getFileRecord",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "input1", "type": "string"},
                    {"internalType": "string", "name": "input2", "type": "string"},
                    {"internalType": "uint256", "name": "integer1", "type": "uint256"},
                    {
                        "internalType": "bytes[]",
                        "name": "fileInputs",
                        "type": "bytes[]",
                    },
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                ],
                "internalType": "struct FileProcessor.FileRecord",
                "name": "",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getTotalFilesProcessed",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalFilesProcessed",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

client = ipfshttpclient.connect()

links = ""

@app.route("/uploader", methods=["POST","GET"])
def upload_files():
    hlink = "https://ipfs.io/ipfs/"
    if request.method == 'POST':
        files = request.files.getlist("files")
        for file in files:
            res = client.add(file)
            print(res)
            print("Hash: ", res.get("Hash"))
            hlink += res.get("Hash")
            print("The link: ", hlink)
            global links
            links = hlink
            create_database(links)


if __name__ == "__main__":
    app.run()
    