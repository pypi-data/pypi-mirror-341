import os
import json

class PrivateKey():
  def __init__(self, secret, modulus=None):
    self.secret = secret
    self.modulus = None
    if modulus is not None:
      self.modulus = modulus


  def save_to_keyfile(self, keyfile_path):
    fp = open(os.path.join(keyfile_path, "sec.lwe.key"))
    data = json.dumps({
      "sec": self.secret
    })
    fp.write(data)
    fp.close()