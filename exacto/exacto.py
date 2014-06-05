class Exon():
    def __init__(self, start, end, chromosome, genome_build, source)
        self.min_pos = min(start, end)
        self.max_pos = max(start, end)
        self.start = start
        self.end = end
        
        self.orientation = "+" if start < end else "-"
        self.genome_build = genome_build

class ExonList():
    def __init__(self, genome_build, source):
        self.genome_build = genome_build
        self.source = source
        self._exons = []

    def addExon(self, exon):
        self._exons.append(exon)


    def listExons():
        return sorted(self._exons, key=lambda x: x.min_pos)


class ExactoClustering():
    def __init__(self):
        pass

    def addExonlist(self):
        pass


    def clusterExons(self):
        """ cluster the exons in the lists that have been added, and
        return a list of ExonClusters """
        # iterate through lists and add exons to graph

        # compare each pair of exons and make edges if overlapping

        # extract connected components and merge into ExonClusters 
       
        pass
    
     

class ExonCluster():
    def __init__(self, span_min, span_max, chromosome, genome_build, source):
        self.


   


    
