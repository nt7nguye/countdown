import os

words = set()
for root, dirs, files in os.walk(os.getcwd()):
    for subdir in dirs:
        word_path = os.path.join(root, subdir, 'words.txt')

        with open(word_path, 'r') as word_file:
            data = word_file.read()
            words = words.union(set(data.split('\n')))

with open('words.txt', 'w') as word_file:
    for w in sorted(list(words)):
        if w.isalnum():
            word_file.write('{}\n'.format(w.lower()))