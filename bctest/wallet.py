# This class instantiates the all users on the network
# Also holds their current wallet

from trans import Transaction
import subprocess

class Wallet:
    def __init__(self, currentNodeName, currentNodeUuid):
        self.allNodes = []
        self.addNode(currentNodeName, currentNodeUuid)
        self.currentNodeUuid = currentNodeUuid

    def addNode(self, name, uuid, miner=False):
        node = {
            "name": name,
            "uuid": uuid,
            "miner": miner,
            "publicKey": None,
            "blocksWithTrans": []
        }

        self.allNodes.append(node)
    
    def getNodes(self):
        return self.allNodes

    def findIndexByUuid(self, uuid):
        for idx in range(len(self.allNodes)):
            if self.allNodes[idx]['uuid'] == uuid:
                return idx
        return false

    def findIndexByName(self, name):
        for idx in range(len(self.allNodes)):
            if self.allNodes[idx]['name'] == name:
                return idx
        return false

    def generateKeys(self):
        subprocess.check_call(["bash", "./genRsaKeys.sh"])
        self.__addPublicKey()

    def __addPublicKey(self):
        with open("public.pub", "r") as file:
            pubKey = file.read()
        pubKey = pubKey.replace("\n", '')
        
        # need to remove the key

        idx = self.findIndexByUuid(self.currentNodeUuid)
        self.allNodes[idx]['publicKey'] = pubKey
        print(self.allNodes[idx])

    def readTransaction(self, blockNum):
        pass

        




    # def findNodeByName(self, name):

wall = Wallet("JPM", 1234)
wall.addNode("BOA", 5678, True)

wall.generateKeys()
print(wall.getNodes())

t = Transaction()