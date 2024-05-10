from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def hash_key(original_key):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(original_key.encode())
    return digest.finalize()

def encrypt(data, key):
    iv = os.urandom(32)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    #print('TAG length:',len(encryptor.tag), encryptor.tag)
    return iv + encrypted_data, encryptor.tag

def decrypt(encrypted_data, key, tag):
    iv = encrypted_data[:32]
    actual_encrypted_data = encrypted_data[32:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(actual_encrypted_data) + decryptor.finalize()
    return decrypted_data.decode('utf-8')