### Author:: Anupriya

import sys

SIZE = 101

## TODO: make dictionary dynamic if the item count increases. right now it is fixed size
class NList:
    def __init__(self, pattern, value):
        self.pattern = pattern
        self.value = value
        self.next = None
    
class HashTable:
    def __init__(self):
        self.hSize = SIZE
        
        self.hTable = []
        for i in range(self.hSize):
            self.hTable.append(NList('/0', '0'))

    def lookup(self, pattern):
        nlist = self.search(pattern)
        if (nlist != None):
            return nlist.value
        else:
            return None
    

    def contains_key(self, pattern):
        return self.search(pattern) != None
    
    def add_or_update(self, pattern, value):
        if (self.contains_key(pattern) == False):
            nlist = self.hTable[self.Hash(pattern)]
            nlist.next = NList(pattern, value)
        else:
            nlist = self.search(pattern);
            nlist.Value = value
    
    def search(self, pattern):
        hash = self.Hash(pattern)
        nlist = self.hTable[hash].next;

        while (nlist != None):
            if (pattern == nlist.pattern):
                return nlist
            nlist = nlist.next;
        return None

    def Hash(self, pattern):
        hashval = 0
        for ch in pattern:
            hashval = ord(ch) + 31 * hashval
        hash = hashval % self.hSize
        
        return hash
    
    
## TODO: if m >> n, where m is no. of patters and n is size of strings
## use suffix array to optimize the implementation
class Scrabble:
    def __init__(self, file_values, file_dict):
        self.file_values = file_values
        self.file_dict = file_dict
        self.value_dict = HashTable()
        
    def create_value_dict(self):
        with open(self.file_values, 'r') as file:
            for line in file:
                line = line.strip('\n')
                word, score = line.split(' ')
                self.value_dict.add_or_update(word, int(score))

    def print_highest_value_words(self):
        self.create_value_dict()
        
        maxValue = 0;
        maxValueWords = []
        with open(self.file_dict, 'r') as file:
            for line in file:
                word = line.strip('\n')
    
                currentValue = 0;
                
                ## TODO: use suffix array to optimize the implementation
                i = 0
                while i < len(word):
                    isPreviousMatch = False
                    previousMatchValue = 0
                    previousMatchPos = 0
            
                    for j in range(i, len(word)):
                        subString = word[i: j-i+1]
                        if (self.value_dict.contains_key(subString) == True):
                            isPreviousMatch = True
                            previousMatchPos = j
                            previousMatchValue = self.value_dict.lookup(subString)
            
                    if (isPreviousMatch == True):
                        i = previousMatchPos + 1
                        currentValue += previousMatchValue
                    else:
                        i += 1
                        
                if (currentValue > maxValue):
                    maxValueWords = []
                    maxValueWords.append(word)
                    maxValue = currentValue
                elif(currentValue == maxValue and maxValue != 0):
                    maxValueWords.append(word)
        for word in maxValueWords:
            print(word + ' ' + str(maxValue))
            
if __name__ == "__main__":
    s = Scrabble(sys.argv[1], sys.argv[2])
    s.print_highest_value_words()
