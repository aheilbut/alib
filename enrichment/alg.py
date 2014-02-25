

import scipy.stats
import statsmodels
import statsmodels.sandbox

import statsmodels.sandbox.stats.multicomp as multicomp
import pandas as pd


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

            overlaps = pd.DataFrame(match_set, 
                                    columns = ["set_name", 
                                               "match_count", 
                                               "intersect_list", 
                                               "size of set"])
    return overlaps 


def calc_overlap_stats(test_set, geneset_dict, total_genes):
    """ get the overlaps and compute hypergeometric stats""" 

    overlaps = get_overlaps(test_set, geneset_dict)

    p = overlaps.apply( lambda x: (
      scipy.stats.hypergeom.sf(
          x.ix["match_count"]-1, # number of differentially expressed genes in set
          total_genes,           # total number of genes
          x.ix["size of set"],   # number of genes in current set
          len( test_set ))),     # total number of genes in test set
                               axis=1)
    p = pd.DataFrame(p, columns=["hypergeom p-val"])
    
    overlaps = overlaps.select(lambda x: overlaps.ix[x, "match_count"] > 0)
    overlaps = overlaps.merge(p, 
                              left_index=True, 
                              right_index=True).sort("hypergeom p-val", ascending=True)

    if len(overlaps.index) > 0:
        overlaps["bonferroni"] = multicomp.multipletests(overlaps.ix[:,"hypergeom p-val"], 
                                                         method="bonferroni")[1]
        overlaps["b-h fdr adj pval"] = multicomp.multipletests(
            overlaps.ix[:,"hypergeom p-val"].fillna(1.0), 
            method="fdr_bh")[1]

    return overlaps.sort("hypergeom p-val", ascending=True)
