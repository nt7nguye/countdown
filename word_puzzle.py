import string 
from typing import List

class TrieNode:
    def __init__(self):
        self.children = [None for _ in range(26)]
        self.isWord = False
    
    def getChildren(self, char: str):
        return self.children[ord(char) - ord('a')]
    
    def createChild(self, char: str):
        self.children[ord(char) - ord('a')] = TrieNode()
    
    def custom_str(self, level=0):
        return_str = ""
        for idx in range(26):
            child = self.children[idx]
            if child is not None:
                return_str += "\t"*level + chr(ord('a') + idx) + "\n" + child.custom_str(level+1)
        return return_str
    
class WordPuzzle:
    def __init__(self, wordList: List[str], rlencode = False, minWordLen = 5, maxWordLen = 15):
        self.wordList = [word.lower() for word in wordList]
        self.root = TrieNode()
        self.solutions = [set() for _ in range(maxWordLen)]
        self.minWordLen = 5
        self.maxWordLen = 15

        if rlencode:
            self.buildRLEncodeTrie()
        else:
            self.buildTrie() 

    def buildRLEncodeTrie(self):
        node = self.root
        stack = []
        for (word) in self.wordList:
            try:
                word_idx = 0
                height = 0
                while word[word_idx].isnumeric():
                    height += height * 10 + int(word[0])
                    word_idx += 1
                while len(stack) > height:
                    stack.pop()
                    node = self.root if len(stack) == 0 else stack[-1]

                for char in word[word_idx:]:
                    if node.getChildren(char) is None:
                        node.createChild(char)
                    node = node.getChildren(char)
                    stack.append(node)
                node.isWord = True
            except:
                raise Exception("Something went wrong adding encoded word" + word)

    def buildTrie(self):
        for (word) in self.wordList:
            try: 
                self.insertTrie(word)
            except:
                raise Exception("Soemthing went wrong adding word" + word)

    def insertTrie(self, word: str):
        node = self.root
        for char in word:
            if node.getChildren(char) is None:
                node.createChild(char)
            node = node.getChildren(char)
        node.isWord = True
    
    def isWord(self, word: str):
        node = self.root
        for char in word:
            if node.getChildren(char) is None:
                return False
            node = node.getChildren(char)
        return node.isWord
    
    def solveRecursive(self, chars: List[str], node: TrieNode, prefix: str = ""):
        for char in chars:
            if node.getChildren(char) is None:
                continue
            childNode = node.getChildren(char)
            if childNode.isWord and len(prefix) + 1 >= self.minWordLen:
                self.solutions[len(prefix) + 1].add(prefix + char)
            if len(chars) > 1 and len(prefix) + 1 < self.maxWordLen:
                charsCopy = chars.copy()
                charsCopy.remove(char)
                self.solveRecursive(charsCopy, childNode, prefix + char)
    
    def solve(self, chars: str):
        self.solveRecursive(list(chars.lower()), node=self.root)
        return self.solutions