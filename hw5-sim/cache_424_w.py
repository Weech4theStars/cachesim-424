
# Write team member names here: liz weech, angela rose west


'''
Base class file for Cache
Credit: R. Martin (W&M), A. Jog (W&M), Ramulator (CMU)
'''

import numpy as np
from math import log2
import random


class Cache:
    def __init__(self, cSize, ways=1, bSize=4):

        self.cacheSize = cSize  # Bytes
        self.ways = ways        # Default: 1 way (i.e., directly mapped)
        self.blockSize = bSize  # Default: 4 bytes (i.e., 1 word block)
        self.sets = cSize // bSize // ways

        self.blockBits = 0
        self.setBits = 0

        if (self.blockSize != 1):
            self.blockBits = int(log2(self.blockSize))

        if (self.sets != 1):
            self.setBits = int(log2(self.sets))

        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=int)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=int)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0
        self.hitlatency = 5 # cycle

    def reset(self):
        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=int)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=int)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0
    '''
    Warning: DO NOT EDIT ANYTHING BEFORE THIS LINE
    '''


    '''
    Returns the set number of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''
    def find_set(self, address):
        # we assume we aren't being given larger than a 64 bit address
        set = np.uint64(address)

        # tagSize = addressSize - blockBits - setBits
        tagSize = 64 - self.blockBits - self.setBits

        # get rid of tag bits
        set = set << np.uint64(tagSize)

        # get rid of appended zeros and blockBits
        set = set >> np.uint64(tagSize + self.blockBits)
        return set


    '''
    Returns the tag of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''
    def find_tag(self, address):
        # get rid of blockBits and setBits
        tag = address >> (self.blockBits + self.setBits)
        return tag

    '''
    Search through cache for address
    return True if found
    otherwise False
    Do NOT change the function definition and arguments
    '''
    def find(self, address):
        set = self.find_set(address)
        tag = self.find_tag(address)
        for i in range(0, self.ways):
            if self.cache[set][i][0] == tag:
                self.hit += 1
                # update metaCache's recent use counter
                self.metaCache[set][i] = self.miss + self.hit
                return True
        self.miss += 1
        return False

    '''
    Load data into the cache.
    Something might need to be evicted from the cache and send back to memory
    Do NOT change the function definition and arguments
    '''
    def load(self, address):
        # check for vacancies
        set = self.find_set(address)
        tag = self.find_tag(address)
        lru = 0
        # search for vacancies while tracking which way is lru
        for i in range(0, self.ways):
            # look for lru
            if self.metaCache[set][i] < self.metaCache[set][lru]:
                lru = i

            if self.cache[set][i][0] == -1:
                self.cache[set][i] = tag
                self.metaCache[set][i] = self.hit + self.miss
                return

        # if no vacancies, kick out least recently used
        self.cache[set][lru] = tag
        # update metaCache's recent use counter
        self.metaCache[set][lru] = self.hit + self.miss
