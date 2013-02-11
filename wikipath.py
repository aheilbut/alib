# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 14:18:31 2013

@author: adrian
"""
from lxml import etree
import pandas as pd
import glob

import scipy.stats
import statsmodels
import statsmodels.sandbox

import alib_local
    
class WikiPathSets():
    def __init__(self):
        self.load_wikipathways_sets()

    def loadGPMLPathways(self, directory):
        files = glob.glob(directory)
        wp_genes = {}
        for f in files:
            tree = etree.parse(open(f))
            root = tree.getroot()
            ids = []
            # stupid datatabase provides pathways in three different namespaces / format versions 
            for node in root.findall('{http://genmapp.org/GPML/2010a}DataNode'):
                xref = node.find('{http://genmapp.org/GPML/2010a}Xref')
                if xref.get("Database") == "Entrez Gene":
                    ids.append(xref.get("ID"))
                if xref.get("Database") == "Ensembl Human":
                    ensembl_id = xref.get("ID")
                    if ensembl_id in self.ensembl_map:
                        ids.append(self.ensembl_map[ensembl_id]) 
                if xref.get("Database") == "UniProt":            
                    uniprot_id = xref.get("ID")
                    if uniprot_id in self.uniprot_idmap:
                        ids.append(self.uniprot_idmap[uniprot_id])

            for node in root.findall('{http://genmapp.org/GPML/2008a}DataNode'):
                xref = node.find('{http://genmapp.org/GPML/2008a}Xref')
                if xref.get("Database") == "Entrez Gene":
                    ids.append(xref.get("ID"))
                if xref.get("Database") == "Ensembl Human":
                    ensembl_id = xref.get("ID")
                    if ensembl_id in self.ensembl_map:
                        ids.append(self.ensembl_map[ensembl_id]) 
                if xref.get("Database") == "UniProt":            
                    uniprot_id = xref.get("ID")
                    if uniprot_id in self.uniprot_idmap:
                        ids.append(self.uniprot_idmap[uniprot_id])


            for node in root.findall('{http://genmapp.org/GPML/2007}DataNode'):
                xref = node.find('{http://genmapp.org/GPML/2007}Xref')
                if xref.get("Database") == "Entrez Gene":
                    ids.append(xref.get("ID"))
                if xref.get("Database") == "Ensembl Human":
                    ensembl_id = xref.get("ID")
                    if ensembl_id in self.ensembl_map:
                        ids.append(self.ensembl_map[ensembl_id]) 
                if xref.get("Database") == "UniProt":            
                    uniprot_id = xref.get("ID")
                    if uniprot_id in self.uniprot_idmap:
                        ids.append(self.uniprot_idmap[uniprot_id])


            wp_genes[root.get("Name")] = ids
        return wp_genes
        
    def loadUniProtMapping(self):
        f = open("/data/adrian/data/uniprot/idmapping.geneid.dat")
        idmap = {}
        for l in f:
            (uniprot, x, geneid) = l.rstrip().split("\t")
            idmap[uniprot] = geneid
        return idmap


    def loadEnsemblMapping(self):
        # tax_id GeneID Ensembl_gene_identifier RNA_nucleotide_accession.version Ensembl_rna_identifier protein_accession.version Ensembl_protein_identifier 
        f = open("/data/adrian/data/ncbigene/gene2ensembl")
        idmap = {}
        for l in f:
            if l[0] == "#":
                pass
            else:
                (tax_id, GeneID, Ensembl_gene_identifier,
                 RNA_nucleotide_accession_version,
                 Ensembl_rna_identifier, protein_accession_version,
                 Ensembl_protein_identifier) = l.rstrip().split("\t")
                idmap[Ensembl_gene_identifier] = GeneID 
        return idmap


    def load_wikipathways_sets(self):
#        self.ensembl_map = self.loadEnsemblMapping()
#        self.uniprot_idmap = self.loadUniProtMapping()
    
        self.gene_info = pd.DataFrame.from_csv(alib_local.datadir + "/gene_info.humanmouse.withHeader.tab", header=0, index_col=None, sep="\t")
    
        symbol_dict = dict(zip( [str(i) for i in self.gene_info["GeneID"]], [str(u).upper() for u in self.gene_info["Symbol"]]) )
    
#        mouse_wp_geneids = self.loadGPMLPathways("/data/adrian/Dropbox/Data/wikipathways/mm/*.gpml")
#        hs_wp_geneids = self.loadGPMLPathways("/data/adrian/Dropbox/Data/wikipathways/hs/gpml/*.gpml")
#        kegg_gs_wp_geneids = self.loadGPMLPathways("/data/adrian/Dropbox/Data/Hsa-KEGG_20110518/*.gpml")
    
        wp_mm = pd.DataFrame.from_csv(alib_local.datadir + "/wp_mm_data.tab", sep="\t")

        mouse_wp_geneids = dict( [(x, str(wp_mm.ix[x, "Entrez Gene"]).split(",")) for x in wp_mm.index] )

        self.mouse_wp_symbols = dict( [(set_name, list(set([symbol_dict[i] for i in gene_ids if i in symbol_dict])) ) 
        for (set_name, gene_ids) in mouse_wp_geneids.items()] )
    
#        self.hs_wp_symbols = dict([(set_name, list(set([symbol_dict[i] for i in gene_ids if i in symbol_dict])) ) 
#        for (set_name, gene_ids) in hs_wp_geneids.items()])
    
#        self.kegg_hs_wp_symbols = dict( [(set_name, list(set([symbol_dict[i] for i in gene_ids if i in symbol_dict])) ) 
#        for (set_name, gene_ids) in kegg_gs_wp_geneids.items()] )
    
    
#        killist = ["XPodNet", "PodNet", "PluriNetWork"]
#        for k in killist:
 #               del self.mouse_wp_symbols[k]
    

    def save_to_GCT(gct_filename):
        gmtfile = open(gct_filename, "w")
        for (key, values) in wp.mouse_wp_symbols.items():
            gmtfile.write( "\t".join( [key.replace(" ", "_"), "http://www.wikipathways.org", "\t".join(values)] ) + "\n")
        gmtfile.close()
    
    def get_wp_geneset_relation(self, symbol_set):
        "return wikipathways sets as a relational table"
        geneset_relation = []
        for (set_name, set_list) in symbol_set.items():
            geneset_relation.extend( [(set_name, gene) for gene in set(set_list)] )
        
        geneset_relation = pd.DataFrame(geneset_relation, columns=["geneset", "genesymbol"])
    
        return geneset_relation





def get_overlaps(test_set, geneset_dict):
    symbol_list = [s.upper() for s in test_set]
    symbol_set = set(symbol_list)

    match_set = []
    for (set_name, set_contents) in geneset_dict.items():
        #    print [s for s in symbol_list if s in set_contents]
        #    print sum([s in set_contents for s in set(symbol_list)]),  symbol_set.intersection(set_contents)
            match_set.append( (set_name,
                               sum([s in set_contents for s in set(symbol_list)]),
                               symbol_set.intersection(set_contents), len(set_contents) ) )

            overlaps = pd.DataFrame(match_set, columns = ["set_name", "match_count", "intersect_list", "size of set"])
    return overlaps 


def calc_overlap_stats(test_set, geneset_dict, total_genes):
    """ get the overlaps and compute hypergeometric stats""" 

    overlaps = get_overlaps(test_set, geneset_dict)

    p = overlaps.apply( lambda x: (
      scipy.stats.hypergeom.sf(
        x.ix["match_count"]-1, # number of differentially expressed genes in set
        total_genes, # total number of genes
        x.ix["size of set"], # number of genes in current set
        len( test_set ))), # total number of differentially expressed genes
     axis=1)
    p = pd.DataFrame(p, columns=["hypergeom p-val"])

    overlaps = overlaps.select(lambda x: overlaps.ix[x, "match_count"] > 0)
    overlaps = overlaps.merge(p, left_index=True, right_index=True).sort("hypergeom p-val", ascending=True)

    if len(overlaps.index) > 0:
        overlaps["bonferroni"] = statsmodels.sandbox.stats.multicomp.multipletests(overlaps.ix[:,"hypergeom p-val"], method="bonferroni")[1]
        overlaps["b-h fdr adj pval"] = statsmodels.sandbox.stats.multicomp.multipletests(overlaps.ix[:,"hypergeom p-val"].fillna(1.0), method="fdr_bh")[1]

    return overlaps.sort("hypergeom p-val", ascending=True)

"""


def printsets():
    htmldata = ""
        cs_annotated = cs.merge( geneset_relation, left_on="symbol_upper", right_on="genesymbol")
            for (g, g_contents) in cs_annotated.groupby("geneset").groups.items():
                    htmldata += (cs_annotated.ix[g_contents, ["probe_id", "symbol", "geneset"]].to_html())
                        return HTML(htmldata)


"""
