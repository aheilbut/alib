import re
import unittest

class MSIGdb():
    def __init__(self, msigdirectory):
        self.genesets = {}
        self.genesetdesc = {}
        
        for gmt in ["msigdb.v3.0.symbols.gmt"]:
            f = open(msigdirectory + "/" + gmt)
            for l in f:
                data = l.rstrip().split("\t")
                self.genesets[data[0].replace('"','')] = data[2:]
                self.genesetdesc[data[0]] = data[1]

        
    def findGenesetsByName(self, query):
        """ return a list of gene set names matching query """
        return [k for k in self.genesets.keys() if re.search(query, k) is not None]
        
    
    def getGenesetAsSymbols(self, genesetname):
        return self.genesets[genesetname]
#    def getGenesetAsHumanEntrezIDs(self, genesetname):
#        pass
    

class testMSIGdb(unittest.TestCase):   
    def testLoaddata(self):
        msig = MSIGdb("/data/adrian/Dropbox/Data/msigDB")

    
if __name__ == "__main__":
    unittest.main()