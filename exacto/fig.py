from alib.graphics.simpleSVG import SVGScene
import exacto
 

class ExonClustFigure():
    def __init__(self, exacto_clustering):
        clusters = exacto_clustering.clusterExons()
        self.exacto_clustering = exacto_clustering
        self.num_segments = len(clusters)
        self.total_bp = sum([c.length() for c in clusters])
        self.sorted_clusters = sorted(clusters, key=lambda x: x.span_min_pos)
    
        self.sources = set()
        for c in self.sorted_clusters:
            for k in c.children.keys():
                self.sources.add(k)
    
        self.scene = SVGScene()
        self.fig_width_px = 1000.0
        self.gutter_width = 15.0

        self.sourcecolors = ["red", "yellow", "green"]
        
        self.horiz_scale = (self.fig_width_px - self.gutter_width * (self.num_segments-1)) / self.total_bp 
        
        self.cluster_min_xpos = {}
        
    def draw(self):
        cur_x_pos = 120.0
        
        self.scene.text((0, 100.20), "all exons", size=10)            
        for i, k in enumerate(self.sources):
            self.scene.text((0, 150.0 + ((i+1) * 15.0)), "%s exons" % k, size=10)            

        for (cluster_index, c) in enumerate(self.sorted_clusters):
            cur_width = c.length() * self.horiz_scale

            self.scene.rectangle((cur_x_pos, 100.0), 30.0, cur_width)

            for i, k in enumerate(self.sources):
                if c.children.has_key(k):
                    
                    for exon in c.children[k].listExons():
                        ex_rel_start = exon.min_pos - c.span_min_pos
                        ex_length = exon.max_pos - exon.min_pos
                        ex_x_pos = cur_x_pos + (ex_rel_start * self.horiz_scale)
                        ex_width = ex_length * self.horiz_scale
                        self.scene.rectangle((ex_x_pos, 150.0 + ((i+1) * 15.0)),
                                             10.0, 
                                             ex_width, 
                                             self.sourcecolors[i])
            
            self.cluster_min_xpos[cluster_index] = cur_x_pos
            cur_x_pos += cur_width + self.gutter_width

    
        y_pos = 250.0
        for transcript in self.exacto_clustering.transcriptModels:
            self.scene.text((0, y_pos), transcript.transcript_accession, size=10)
            
            for exon in transcript.listExons():                    
                # get the cluster this exon belongs to
                matching_cluster = self.exacto_clustering.index[(exon.source, exon.min_pos, exon.max_pos)] 
                # get the cluster_id 
                matching_cluster_id = self.exacto_clustering.cluster_id_index[matching_cluster]
                # get the start of this cluster's column
                cluster_min_xpos = self.cluster_min_xpos[matching_cluster_id]
                # draw bar for this exon
                
                ex_rel_start = exon.min_pos - matching_cluster.span_min_pos
                ex_length = exon.max_pos - exon.min_pos
                
                ex_quant_xpos = cluster_min_xpos + (ex_rel_start * self.horiz_scale)
                ex_quant_width = ex_length * self.horiz_scale
                
                ex_quant_height = 10.0
                
                self.scene.rectangle( (ex_quant_xpos, y_pos-ex_quant_height), ex_quant_height, ex_quant_width, color='gray')
    
            y_pos += 15.0


        y_pos += 100.0
        bar_height = 30.0
        for quant_set in self.exacto_clustering.exonQuantSets:
            
            self.scene.text((0, y_pos), quant_set.context_description, size=10)
            
            for exon in quant_set.listExons():
                # get the cluster this exon belongs to
                matching_cluster = self.exacto_clustering.index[(exon.source, exon.min_pos, exon.max_pos)] 
                # get the cluster_id 
                matching_cluster_id = self.exacto_clustering.cluster_id_index[matching_cluster]
                # get the start of this cluster's column
                cluster_min_xpos = self.cluster_min_xpos[matching_cluster_id]
                # draw bar for this exon
                
                ex_rel_start = exon.min_pos - matching_cluster.span_min_pos
                ex_length = exon.max_pos - exon.min_pos
                
                ex_quant_xpos = cluster_min_xpos + (ex_rel_start * self.horiz_scale)
                ex_quant_width = ex_length * self.horiz_scale
                
                ex_quant_height = min( 30.0, bar_height * exon.expression_value / quant_set.max_quant_value )
                
                self.scene.rectangle( (ex_quant_xpos, y_pos-ex_quant_height), ex_quant_height, ex_quant_width, color='red')
                
            y_pos += 60.0