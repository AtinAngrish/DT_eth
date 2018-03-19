#import time
from web3 import Web3, RPCProvider
from os import path
import requests
import json
import random

class ContractHandler:
    def __init__(self):
        # Load contract configuration
        self.web3 = Web3(RPCProvider(host='localhost', port='8545'))
        dir_path = path.dirname(path.realpath(__file__))
        with open(str(path.join(dir_path, 'Config.txt')), 'r') as configuration:
            for line in configuration:
                if line.startswith('contract='):
                    self.contract_address = line.split('=')[1].rstrip('\n')
                if line.startswith('trading_account='):
                    self.trading_account = line.split('=')[1].rstrip('\n')
                if line.startswith('trading_password='):
                    self.trading_password = line.split('=')[1].rstrip('\n')
                # Simulate trading by having a mining account to transfer ether
                if line.startswith('mining_account='):
                    self.mining_account = line.split('=')[1].rstrip('\n')
                if line.startswith('mining_password='):
                    self.mining_password = line.split('=')[1].rstrip('\n')
        with open(str(path.join(dir_path, 'contract_abi.json')), 'r') as abi_definition:
            self.abi = json.load(abi_definition)
        self.contract = self.web3.eth.contract(self.abi, self.contract_address)#

    def sellHours(self, address, machin_no, hours):
        #function sellHours(address _seller,uint _mno, uint _hours) public returns(string){
        txid = self.contract.transact().sellHours(address, machin_no, hours)
        return txid

    def addMachine(self, name, mac, avalibleTime, rate):
        #function addMachine(string _name,string _mac,uint availableTime,uint _mRate) public returns(string){
        print("Logon Succesful: ", self.web3.personal.unlockAccount(self.mining_account, 
                                                                    self.mining_password
                                                                    ))
        txid = self.contract.transact().addMachine(name, mac, avalibleTime, rate)
        return txid

    def addUser(self):
        #function addUser() public{
        print("Logon Succesful: ", self.web3.personal.unlockAccount(self.mining_account, self.mining_password))
        txid = self.contract.transact().addUser()
        return txid

    def getMachineInfo(self, address, number):
        #function getMachineInfo(address vadd,uint num) public constant returns (string ,bool,uint,string){
        #machine no's start at 0
        #response = self.contract.call().getMachineInfo(address, number)
        return self.contract.call().getMachineInfo(address, number)
        #return response

    def updateMachineStatus(self, user, mac, stat, time, rate):
        #function updateMachineStatus(address reqUser,string _mac, bool _stat, uint _availTime,uint _mRate) public{
        print("Logon Succesful: ", self.web3.personal.unlockAccount(self.trading_account, self.trading_password))
        txid = self.contract.transact().updateMachineStatus(user, mac, stat, time, rate)
        return txid
    
    def getNoMachines(self,address):
        #function getNumberOfMachines(address vadd) constant public returns  (uint)
        return self.contract.call().getNumberOfMachines(address)

    def test(self):
        print("test")

if __name__ == '__main__':
    CH = ContractHandler()
    print(CH.getNoMachines(CH.trading_account))
    print(CH.getMachineInfo(CH.trading_account,0))
    CH.updateMachineStatus(CH.trading_account,"AAA",False,21,18)

