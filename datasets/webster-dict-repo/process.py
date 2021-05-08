# Convert the json file into text file

import json

with open('dictionary.json', 'r') as my_file:
    data = my_file.read()

dictionary = json.loads(data)

with open('words.txt', 'w') as word_file:
    # Remove duplicates
    words = list(set(dictionary.keys()))

    # Write out
    for w in words:
        if w.isalnum():
            word_file.write(f'{w.lower()}\n')
