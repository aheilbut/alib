import datetime
import scipy.cluster
import pylab, matplotlib
import fastcluster


# set up blue red color map 
cdict = { 'red': ((0.0, 0.0, 0.0), 
                (0.5, 1.0, 1.0),
                (1.0, 1.0, 1.0)),
          'green' : ((0.0, 0.0, 0.0),
               (0.5, 1.0, 1.0),
               (1.0, 0.0, 0.0)),
          'blue' : ((0.0, 1.0, 1.0),
                  (0.5, 1.0, 1.0),
                  (1.0, 0.0, 0.0))}
my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 256)
my_cmap.set_bad("0.9")

def clusterHeatmap(df, title, row_label_map, col_label_map, colormap=my_cmap, 
                   cluster_rows=False, cluster_columns=False, cluster_data=None,
                   row_dendrogram=False, column_dendrogram=False, width=30, height=20, vmin=-3, vmax=3, distmethod="correlation", colorbar=True, colorbar_shrink=0.2):

    cm = pylab.get_cmap(colormap)
    cm.set_bad("0.9")

    # do clustering 
    if cluster_data is None:
        cluster_data = df # cluster the same data that we are plotting    

    matplotlib.rcParams['figure.figsize'] = [width, height]    
    #    pylab.figsize(20, 10)
    pylab.title(title)
#    pylab.text(0,-5,str(datetime.date.today()))
    
    # ylabels = [genesym[geneid] for geneid in pt.axes[0][Z['leaves']]]
    #  xlabels = pt.axes[1][cZ['leaves']]
    
    orderedVal = df
    
    if cluster_rows:
        distances = scipy.cluster.hierarchy.distance.pdist(cluster_data.values, distmethod)
        rowY = fastcluster.linkage(distances)
        rowZ = scipy.cluster.hierarchy.dendrogram(rowY, orientation='right', no_plot=True)
        orderedVal = df.reindex(index=df.axes[0][rowZ['leaves']])

        
    if cluster_columns:
        coldist = scipy.cluster.hierarchy.distance.pdist(df.values.transpose(), distmethod)
        cY = scipy.cluster.hierarchy.linkage(coldist)
        cZ = scipy.cluster.hierarchy.dendrogram(cY, no_plot=True)    
        orderedVal = orderedVal.reindex(columns=df.axes[1][cZ['leaves']])
    
    # row labels 
    if row_label_map is not None:
        pylab.yticks(range(0, len(orderedVal.index)), [row_label_map[i] for i in orderedVal.index])        
    else:
        pylab.yticks(range(0, len(orderedVal.index)), orderedVal.index)
    pylab.xticks(range(0, len(orderedVal.columns)), orderedVal.columns, rotation=90)

    
    if col_label_map is not None:
        pylab.xticks(range(0, len(orderedVal.columns)), [col_label_map[i] for i in orderedVal.columns])                
    
    #orderedVal = orderedVal[:,]
    pylab.tick_params(direction="out")
    pylab.imshow(orderedVal, interpolation="nearest", cmap=cm, aspect='auto', norm=None, vmin=vmin, vmax=vmax)
    if colorbar:
        pylab.colorbar(shrink=colorbar_shrink)
    #hcluster.dendrogram(Y, orientation='top')
