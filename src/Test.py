from datetime import datetime
from time import time
from Cryptography import Cryptography

cryptograph = Cryptography(5)
message = open("../data/plaintext/50words.txt", "r").read()
key = cryptograph.generate_random_key()
print(key)
cipher = cryptograph.encrypt(message, key)
start = time()
decrypt_key = cryptograph.genetic_decrypt_cipher(cipher)
end = time()
print(decrypt_key)
print(cryptograph.decrypt_mono_substitution(cipher, decrypt_key))
print(end - start)