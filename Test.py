from io import open_code
import os
import json

PATH = "./data/ngrams"
files = os.listdir("./data/ngrams")

for file in files:
    with open(os.path.join(PATH, file), "r") as f:
        message = f.read()
        lines = message.strip().split("\n")
        json_ngrams = {}

        for line in lines:
            k, v = line.split(" ")
            json_ngrams[k] = int(v)
            
        json.dump(json_ngrams, open(f"./data/{os.path.splitext(file)[0]}.json", 'w'))