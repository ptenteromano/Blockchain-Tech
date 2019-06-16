
# coding: utf-8

# In[1]:


# Philip Tenteromano
# 6/11/2019
# Blockchain Tech
# HW 1 

# Using Python3
# Output is saved as a PDF


# ### Problem 4
# #### Mining with the Nonce

# In[2]:


from hashlib import sha256
from timeit import default_timer as timer


# In[3]:


# Dictionary of Difficulty Targets
# 3, 4, or 6 leading 0's
difficultyDict = {
    "EasyMode": "000",
    "HaveFun!": "0000",
    "NowYouWorking!": "000000"
}


# In[4]:


# Simple Block class
class Block:
    def __init__(self, data=""):
        self.data = data
        
    def printData(self):
        print(self.data)


# In[5]:


# Miner Class implements the msg, the hashing, and the comparing
class Miner:
    
    # Initialize the miner with the Nonce
    def __init__(self):
        self.nonce = -1
    
    # Increments the Nonce and concats with the Data, and encoded for hashing
    def dataToBeHashed(self, Block):
        self.nonce += 1
        return (str(self.nonce) + str(Block.data)).encode('utf-8')
    
    # Hash until we found a winner
    def mineNewBlock(self, Block, difficulty):
        self.nonce = -1

        # Start Timer
        start = timer()
        while True:
            msg = self.dataToBeHashed(Block)

            # Need a new hasher object each iteration (or else it will be hash(hash(hash))...)
            newHasher = sha256()
            newHasher.update(msg)

            getHash = newHasher.hexdigest()

            if self.checkTrue(getHash, difficulty):
                end = timer()
                print("YOU DID IT!\nDifficulty = " + str(len(difficulty)) +" leading 0's" )
                print("The Nonce = " + str(self.nonce))
                print(getHash)
                print("\tTotal time: " + str(end - start) + '\n')
                return 
    
    # Checks the leading numbers of 0's against the target (difficulty)
    def checkTrue(self, attempt, target):
        return attempt[:len(target)] == target


# In[6]:


exampleBlock = Block("hello")


# In[7]:


exampleBlock.printData()


# ## Start mining!

# In[8]:


theGreatestMiner = Miner()

# Loop through the difficulties and solve!
for key in difficultyDict.keys():
    theGreatestMiner.mineNewBlock(exampleBlock, difficultyDict[key])


# In[9]:


# Requiring more leading 0's drastically increases time to solve

