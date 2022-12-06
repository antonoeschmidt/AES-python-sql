# Using pycryptodome for Crypto
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sys

ROUNDS=3000000

class AESCipher:
    def __init__(self, password, salt):
        self.key = PBKDF2(password.encode('utf8'), salt.encode('utf8'), 32, count=ROUNDS, hmac_hash_module=SHA512)

    def encrypt(self, data):
        iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + self.cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

    def decrypt(self, data):
        self.cipher = AES.new(self.key, AES.MODE_CBC, data[:AES.block_size])
        try:
            return unpad(self.cipher.decrypt(data[AES.block_size:]), AES.block_size)
        except ValueError:
            sys.exit("Could not decrypt data")

if __name__ == '__main__':
    print('TESTING ENCRYPTION')
    msg = input('Message...: ')
    pwd = input('Password..: ')
    cte = AESCipher(pwd,"SALT").encrypt(msg)
    print('Ciphertext:', repr(cte))

    print('\nTESTING DECRYPTION')
    pte = AESCipher(pwd,"SALT").decrypt(cte).decode('utf-8')
    print('Message...:', pte)