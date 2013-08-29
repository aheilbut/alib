import pandas
import alib_local

class CPDB():
    def __init__(self):
        self.load_cpdb()
    
    def load_cpdb(self):
        """ load human cpdb gene sets into a dict of sets of entrez gene ids """
        self.cpdb_geneid = {}
        self.cpdb_uppersym = {}
        
        gene_info = pandas.DataFrame.from_csv(alib_local.datadir + "/gene_info.humanmouse.withHeader.tab", 
                                          header=0, 
                                          index_col=None, 
                                          sep="\t")        
        entrez_geneid_symbols = dict( [(geneid, str(symbol).upper()) 
                                       for (i, geneid, symbol) 
                                       in gene_info[["GeneID","Symbol"]].to_records()] )
        
        
        for linenum, l in enumerate(open("/data/adrian/Dropbox/Data/CPDB/CPDB_pathways_genes.tab")):
            if linenum > 1:
                (set_name, collection, entrez_ids) = l.split("\t")
                entrez_ids = set( [int(i) 
                                   for i 
                                   in entrez_ids.split(",")] )

                self.cpdb_geneid.setdefault(collection, {})[set_name] = entrez_ids
                self.cpdb_uppersym.setdefault(collection, {})[set_name] = set( [entrez_geneid_symbols[i] 
                                                                                for i 
                                                                                in entrez_ids 
                                                                                if i in entrez_geneid_symbols] )
    
    def get_SYMBOL_matches(self, t):
        matches = []
        t = set(t)
    

        for (k, pathway_geneids) in self.cpdb_uppersym["Wikipathways"].items():
            intersect_set = t.intersection(pathway_geneids)
            matches.append((k, len(intersect_set), len(pathway_geneids), intersect_set ))
            
        return pandas.DataFrame( matches, 
                                 columns=["k", 
                                          "count", 
                                          "set_size", 
                                          "intersection"] ).sort_index(by="count", 
                                                                       ascending=False)[0:10]
