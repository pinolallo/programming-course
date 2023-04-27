"""
********************************************************
*    __            __ ______     __   __               *
*   / /  ___ ____ / //_  __/__ _/ /  / /__ ___         *
*  / _ \/ _ `(_-</ _ \/ / / _ `/ _ \/ / -_|_-<         *
* /_//_/\_,_/___/_//_/_/  \_,_/_.__/_/\__/___/         *
* v 1.1 written by Karandeep Grover                    *
* modified by Silvestro Di Pietro                      *
* a python simple explanation for hashTabling.         *
*                                                      *
********************************************************
"""
class HashTable:  
    def __init__(self,tableSize=10):
        self.tableSize = tableSize
        self.table = [[] for i in range(self.tableSize)]
        
    def get_hash(self, key):
        hash = 0
        charKey=[]
        keySize=len(str(key))
        charKey = [None for i in range(4)]
        #we will take 4 bytes to setup the hash
        # the first 2 bytes and the last 2 bytes (getting the ascii value with ord)
        #if the keySize is 3 the middle value will be the same in charkey[1] and  charkey[2]
        if keySize < 3:
            key=key.ljust(3,'0')
            keySize=len(str(key))
        charKey[0]=key[0]
        charKey[1]=key[1]
        charKey[2]=key[keySize-2]
        charKey[3]=key[keySize-1]
        for char in charKey:
            hash += ord(char)
        #the index generated will be has mod  tablesize
        return hash % self.tableSize
    
    def __getitem__(self, key):
        table_index = self.get_hash(key)
        for kv in self.table[table_index]:
            if kv[0] == key:
                return kv[1]
         
            
    def __setitem__(self, key, val):
        table_index = self.get_hash(key)
        update = False
        #no entries for this index
        if not self.table[table_index]:
            self.table[table_index]=[[key,val]]
        else:
            #chek for an update
            for idx, element in enumerate(self.table[table_index]):
                  #is an update
                if element[0] == key:
                    self.table[table_index][idx]=(key,val)
                    update  = True
                    break
            #not a new entry and not an update: is a collision
            if not update:
                #add key val element
                self.table[table_index].append([key,val])

    def __delitem__(self, key):
        table_index = self.get_hash(key)
        for idx, kv in enumerate(self.table[table_index]):
            if kv[0] == key:
                del self.table[table_index][idx]