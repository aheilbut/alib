import networkx as nx

class Exon():
    def __init__(self, start, end, chromosome, genome_build, source):
        self.min_pos = min(start, end)
        self.max_pos = max(start, end)
        self.start = start
        self.end = end
        self.chromosome = chromosome
                
        self.orientation = "+" if start < end else "-"
        self.genome_build = genome_build
        self.source = source

    def __repr__(self):
        return "%s: %d - %d" % (self.chromosome, self.min_pos, self.max_pos)

    def checkOverlap(self, y):
        # 1
        if (self.chromosome == y.chromosome 
            and self.min_pos == y.min_pos 
            and self.max_pos == y.max_pos):
            return True
        # 2
        elif ( self.chromosome == y.chromosome
               and y.min_pos >= self.min_pos and y.max_pos <= self.max_pos):
            return True
        # 3
        elif ( self.chromosome == y.chromosome
               and y.min_pos <= self.min_pos
               and self.max_pos >= y.min_pos and self.max_pos <= y.max_pos):
            return True
        # 4
        elif ( self.chromosome == y.chromosome
               and self.min_pos >= y.min_pos and self.min_pos <= y.max_pos
               and self.max_pos <= y.max_pos and self.max_pos >= y.min_pos):
            return True
        # 5
        elif ( self.chromosome == y.chromosome
               and self.min_pos >= y.min_pos and self.max_pos <= y.max_pos ):
            return True
        
        else:
            return False


class ExonList():
    def __init__(self, genome_build, source):
        self.genome_build = genome_build
        self.source = source
        self._exons = []

    def addExon(self, exon):
        self._exons.append(exon)

    def listExons(self):
        return sorted(self._exons, key=lambda x: x.min_pos) 
    
    def __repr__(self):
        return str( self._exons )

class ExonCluster():
    def __init__(self):
        self.children = {}
        self.index = {}
        self.span_min_pos = None
        self.span_max_pos = None
        self.orientation = None
        
        

    def __repr__(self):
        return "%d %d %s" % (self.span_min_pos, self.span_max_pos, str(self.children))
    
    def addExon(self, exon):
        if self.span_min_pos is None or exon.min_pos < self.span_min_pos:
            self.span_min_pos = exon.min_pos
            
        if self.span_max_pos is None or exon.max_pos > self.span_max_pos:
            self.span_max_pos = exon.max_pos
            
        if self.orientation is None:
            self.orientation = exon.orientation
            
        if self.children.has_key(exon.source):
            self.children[exon.source].addExon(exon)
        else:
            self.children[exon.source] = ExonList(exon.genome_build, exon.source)
            self.children[exon.source].addExon(exon)
    
    def length(self):
        return self.span_max_pos - self.span_min_pos
    
    

class ExonQuant(Exon):
    def __init__(self, start, end, chromosome, genome_build, source, context_id, expression_value):
        Exon.__init__(self, start, end, chromosome, genome_build, source)
        self.context_id = context_id
        self.expression_value = expression_value
        
class ExonQuantSet(ExonList):
    def __init__(self, genome_build, source, context_id, context_description, context_keys,
                 max_quant_value, min_quant_value):
        ExonList.__init__(self, genome_build, source)
        self.context_id = context_id
        self.context_description = context_description
        self.context_keys = context_keys
        self.max_quant_value = max_quant_value
        self.min_quant_value = min_quant_value

class TranscriptModel(ExonList):
    def __init__(self, genome_build, source, transcript_accession, chromosome, strand, 
                 tx_start, tx_end, cds_start, cds_end, exon_count, transcript_sequence=None):
        ExonList.__init__(self, genome_build, source)
        
        self.transcript_accession = transcript_accession
        self.chromosome = chromosome
        self.strand = strand
        self.tx_start = tx_start
        self.tx_end = tx_end
        self.cds_start = cds_start
        self.cds_end = cds_end
        self.exon_count = exon_count
        self.transcript_sequence = transcript_sequence
        
    


class ExactoClustering():
    def __init__(self):
        self.exonlists = []
        self.clusters = []
        self.index = {}
        self.cluster_id_index = {}

        self.exonQuantSets = []
        self.transcriptModels = []

    def addExonlist(self, el):
        self.exonlists.append(el)


    def clusterExons(self):
        """ cluster the exons in the lists that have been added, and
        return a list of ExonClusters """
        # iterate through lists and add exons to graph
        g = nx.Graph()
        
        for el in self.exonlists:
            g.add_nodes_from( el.listExons() )

        # compare each pair of exons and make edges if overlapping
        for x in g.nodes():
            for y in g.nodes():
                if x.checkOverlap(y):
                    g.add_edge(x, y)

        self.clusters = []
        # extract connected components and merge into ExonClusters 
        for component in nx.connected_components(g):
            ec = ExonCluster()
            for exon in component:
                ec.addExon(exon)                
                self.index[ (exon.source, exon.min_pos, exon.max_pos) ] = ec
                
            self.clusters.append(ec)
        
        # sort the clusters, so each has a consistent index
        self.clusters = sorted(self.clusters, key=lambda x: x.span_min_pos)
        self.cluster_id_index = dict([ (a[1], a[0]) for a in enumerate(self.clusters)])
        return self.clusters
    
    
    def addExonQuantSet(self, exon_quant_set):
        self.exonQuantSets.append(exon_quant_set)
        
    def addTranscriptModel(self, transcriptModel):
        self.transcriptModels.append(transcriptModel)
        

#

   


    
