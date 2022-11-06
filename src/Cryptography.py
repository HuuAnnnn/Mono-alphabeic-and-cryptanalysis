from collections import defaultdict
import itertools
import re
import math
import random
from pathlib import Path
import os
import json

from tqdm import tqdm


class Cryptography:
    __ALPHABET = [chr(char) for char in range(65, 91)]
    __NGRAM = None
    __NGRAMS_MAP = {
        1: "unigrams",
        2: "bigrams",
        3: "trigrams",
        4: "quadgrams",
        5: "quintgrams",
    }

    def __init__(self, ngrams: int) -> None:
        if not self.__NGRAM:
            self.__ngrams = ngrams

            if ngrams not in self.__NGRAMS_MAP.keys():
                ngrams_mapped = "bigram"
            else:
                ngrams_mapped = self.__NGRAMS_MAP[ngrams]

            CUR_PATH = Path(__file__).parent
            ngrams_path = os.path.join(CUR_PATH, f"../data/ngrams/{ngrams_mapped}.json")
            self.__NGRAMS = self.__load_ngrams(ngrams_path)

    def __load_ngrams(self, path):
        return json.load(open(path, "r"))

    def encrypt(self, message: str, key: list) -> str:
        """'
        Using Mono-alphabetic substitution cipher to encrypt message
        """
        cipher = message.lower()
        for i in range(26):
            cipher = cipher.replace(self.__ALPHABET[i].lower(), key[i])

        return cipher

    def decrypt(self, cipher: str, iterates: int = 1000) -> tuple:
        """
        Decrypt Mono-alphabetic substitution using Stochastic Hill Climbing
        """
        max = -math.inf
        decrypted_cipher = ""
        decrypted_key = []
        key = []
        for _ in range(10):
            key_score, key, plaintext = self.decrypt_hillclimbing(cipher, iterates)
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

    def create_chromosome(self):
        return self.generate_random_key()

    def create_population(self, size: int = 5):
        return [self.create_chromosome() for _ in range(size)]

    def selection(self, population, cipher_text):
        score_population = {}
        for i in range(len(population)):
            individual = population[i]
            decrypt_text = self.decrypt_mono_substitution(cipher_text, individual)
            score_population[i] = (self.score(decrypt_text.upper()), individual)

        return sorted(score_population.items(), key=lambda x: x[1][0], reverse=True)

    def genetic_decrypt_cipher(self, cipher_text):
        p_bar = tqdm(range(1, 1001), desc="Process")
        population = self.create_population(20)
        num_of_offspring = 1000

        for i in range(num_of_offspring):
            selection = self.selection(population, cipher_text)
            p_bar.set_description(f"Offspring {i + 1}: {selection[0][1][0]}")
            best_parent = [(population[selection[0][0]], population[selection[1][0]])]
            best_parent += random.sample(list(itertools.permutations(population, 2)), 8)
            offsprings = []
            for pair in best_parent:
                parent_1, parent_2 = pair
                child1, child2 = tuple(self.cross_over(parent_1, parent_2))
                self.mutation(child1, 2e-5)
                self.mutation(child2, 2e-5)
                offsprings.extend([parent_1, parent_2, child1, child2])

            population = offsprings
            p_bar.update(1)

        return self.selection(population, cipher_text)[0][1][1]

    def cross_over(self, parent_1, parent_2, cross_over_rate: float = 0.5):
        cutting_point = int(cross_over_rate * len(parent_1))

        offspring1 = parent_1[0:cutting_point]
        offspring2 = parent_2[0:cutting_point]

        rest_parent_1 = [
            "" if gene in offspring1 else gene for gene in parent_2[cutting_point::]
        ]

        rest_parent_2 = [
            "" if gene in offspring2 else gene for gene in parent_1[cutting_point::]
        ]

        random_letters = random.sample(
            set(self.__ALPHABET)
            .difference(set(offspring2))
            .difference(set(rest_parent_1)),
            rest_parent_1.count(""),
        )
        k = 0
        for i in range(len(rest_parent_1)):
            if rest_parent_1[i] == "":
                rest_parent_1[i] = random_letters[k]
                k += 1

        random_letters = random.sample(
            set(self.__ALPHABET)
            .difference(set(offspring1))
            .difference(set(rest_parent_2)),
            rest_parent_2.count(""),
        )

        k = 0
        for i in range(len(rest_parent_2)):
            if rest_parent_2[i] == "":
                rest_parent_2[i] = random_letters[k]
                k += 1

        offspring1 += rest_parent_2
        offspring2 += rest_parent_1

        return [offspring1, offspring2]

    def mutation(self, chromosome, mutation_rate: float = 0.1):
        num_mutate_genes = int(mutation_rate * len(chromosome))
        for _ in range((num_mutate_genes // 2) + 1):
            self.swap_randomly_2_pos(chromosome)

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
