import re
import math
import random
from datetime import datetime
from pathlib import Path
import os


class Cryptography:
    __ALPHABET = [chr(char) for char in range(65, 91)]
    __NGRAM = None
    __NGRAMS_MAP = {
        1: "unigram",
        2: "bigram",
        3: "trigram",
        4: "quadgram",
        5: "quintgrams",
    }

    def __init__(self, ngrams: int) -> None:
        if not self.__NGRAM:
            self.__ngrams = ngrams

            if ngrams not in self.__NGRAMS_MAP.keys():
                ngrams_mapped = "bigram"
            else:
                ngrams_mapped = self.__NGRAMS_MAP[ngrams]

            CUR_PATH = Path(__file__).parent.parent
            ngrams_path = os.path.join(CUR_PATH, f"data/ngrams/{ngrams_mapped}.txt")
            self.__NGRAMS = self.__load_ngrams(ngrams_path)

    def __load_ngrams(self, path):
        ngram_dict = {}
        message = ""
        with open(path, "r") as f:
            message = f.read()

        ngrams = message.strip().split("\n")

        for ngram in ngrams:
            key_ngram, count = tuple(ngram.split(" "))
            ngram_dict[key_ngram] = int(count)

        return ngram_dict

    def encrypt(self, message: str, key: list) -> str:
        """'
        Using Mono-alphabetic substitution cipher to encrypt message
        """
        cipher = message.lower()
        for i in range(26):
            cipher = cipher.replace(self.__ALPHABET[i].lower(), key[i])

        return cipher

    def decrypt(self, cipher: str) -> tuple:
        """
        Decrypt Mono-alphabetic substitution using Stochastic Hill Climbing
        """
        max = -math.inf
        decrypted_cipher = ""
        decrypted_key = []
        key = []
        for _ in range(10):
            key_score, key, plaintext = self.decrypt_hillclimbing(cipher, 1000)
            if key_score > max:
                max = key_score
                decrypted_cipher = plaintext
                decrypted_key = key

        return (decrypted_cipher, decrypted_key)

    def decrypt_hillclimbing(self, cipher_text: str, N: int) -> tuple:
        """
        Using Stochastic Hill Climbing to find the best key
        """

        key = self.generate_random_key()
        plain_text = self.decrypt_mono_substitution(cipher_text, key)
        key_score = self.score(plain_text.upper())
        period = 0

        while period < N:
            modify_key = self.swap_randomly_2_pos(key.copy())
            plain_text = self.decrypt_mono_substitution(cipher_text, modify_key)
            modify_key_score = self.score(plain_text.upper())

            if modify_key_score > key_score:
                key = modify_key.copy()
                key_score = modify_key_score
                period = 0
            else:
                period += 1

        return (key_score, key, self.decrypt_mono_substitution(cipher_text, key))

    def decrypt_mono_substitution(self, cipher: str, key: list) -> str:
        """
        Decrypt MSC with key
        """
        message = cipher
        for i in range(26):
            message = message.replace(key[i], self.__ALPHABET[i].lower())

        return message

    def generate_random_key(self):
        return random.sample(self.__ALPHABET, 26)

    def swap_randomly_2_pos(self, char_list):
        tmp = char_list
        idx1, idx2 = tuple(random.sample(range(len(char_list)), 2))
        tmp[idx1], tmp[idx2] = tmp[idx2], tmp[idx1]

        return tmp

    def score(self, text):
        ngrams = self.__slice_ngram(text)
        sum = 0
        count = 0

        for ngram in ngrams:
            if ngram in self.__NGRAMS.keys():
                count = self.__NGRAMS[ngram.upper()]
            else:
                count = 1

            sum += math.log2(count)

        return sum / len(set(ngrams))

    def __slice_ngram(self, text):
        cipher = re.sub("[^a-zA-Z]", "", text)
        return [
            cipher[i : i + self.__ngrams] for i in range(len(cipher) - (self.__ngrams))
        ]
