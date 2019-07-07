import subprocess

class Sender:
  def __init__(self, nameId, wallets):
    self.name = nameId
    self.rsaPubKey = wallets[nameId]
    self.currentWallets = wallets

  def findReceiver(self, receiverId):
    self.receiver = receiverId
    self.rcvrRsaPubKey = self.currentWallets[receiverId]

  def encryptDocWithAes(self, file):
    pass

  def _uploadDocument(self, file):
    pass
    