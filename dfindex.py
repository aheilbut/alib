# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:42:41 2014

@author: adrian
"""


def uniquify(l):
    tempset = set([])
    result = []
    for e in l:
        if e not in tempset:
            result.append(e)
            tempset.add(e)
    return result


class PrefixIndex(object):
    def index_prefixes(self, key, term):
        prefixes = [term[0:n] for n in range(len(term), 1, -1)]
        for p in prefixes:
            if self.index.has_key(p):
                self.index[p].append(key)
            else:
                self.index[p] = [key]

    def __init__(self, df, fieldlist):
        self.index = {}
        
        for f in fieldlist:
            for key in df.sort_index(by=fieldlist[0], ascending=True).index:
                for term in df.ix[key, f].lower().split():
                    self.index_prefixes(key, term)
                
        for key in self.index.keys():
            self.index[key] = uniquify( self.index[key] )
    
    
    def __getitem__(self, k):
        return self.index[k]
    
    
    def has_key(self, k):
        return self.index.has_key(k)