import os
from pathlib import Path
import re
from context import src
from src.Cryptography import Cryptography
from datetime import datetime
import argparse

ITERATE = 350


class TestCryptography:
    def __init__(self) -> None:
        self.__n_grams, self.__length = self.args_stmt()
        self.__crypto = Cryptography(ngrams=self.__n_grams)

    def args_stmt(self):
        path = Path(__file__).parent.parent
        data_path = os.path.join(path, "data/plaintext")
        samples = [int(re.findall("\d+", text)[-1]) for text in os.listdir(data_path)]
        parser = argparse.ArgumentParser()
        parser.add_argument("-ng", "--ngrams", help="Enter ngrams you need to test")

        parser.add_argument(
            "-l", "--length", help="Length of the paragraph which you want to test"
        )

        args = parser.parse_args()

        n_grams = int(args.ngrams) if args.ngrams else 2
        length = int(args.length) if args.length else 50

        if n_grams > 5 or n_grams < 1:
            n_grams = 2

        if length not in samples:
            length = 50

        return n_grams, length

    def __call__(self):
        CUR_PATH = Path(__file__).parent.parent
        message_path = os.path.join(
            CUR_PATH, f"data/plaintext/{self.__length}words.txt"
        )

        now = datetime.now()

        print(f"Length: {self.__length}, ngrams: {self.__n_grams}")
        key = self.__crypto.generate_random_key()
        message = open(message_path, "r").read()
        cipher = self.__crypto.encrypt(message, key)

        plain_text, _ = self.__crypto.decrypt(cipher=cipher, iterates=ITERATE)
        count = 0

        plain_words = plain_text.split()
        message_words = message.strip().split()
        for i in range(len(plain_words)):
            if message_words[i].lower() == plain_words[i].lower():
                count += 1

        print(f"{' '.join(plain_words[0 : int(0.1*len(plain_words))])}...")
        print(
            f"{(datetime.now() - now)}: {count/len(message_words)}, {count}/{len(message_words)}"
        )
