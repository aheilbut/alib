import datetime
import scipy.cluster
import pylab, matplotlib


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

def clusterHeatmap(df, title, row_label_map, col_label_map, colormap="YlGn", 
                   cluster_rows=False, cluster_columns=False,
                   row_dendrogram=False, column_dendrogram=False):

    cm = pylab.get_cmap(colormap)
    cm.set_bad("0.9")

    # do clustering 
    
    matplotlib.rcParams['figure.figsize'] = [30, 20]    
    #    pylab.figsize(20, 10)
    pylab.title(title)
    pylab.text(0,-5,str(datetime.date.today()))
    
    # ylabels = [genesym[geneid] for geneid in pt.axes[0][Z['leaves']]]
    #  xlabels = pt.axes[1][cZ['leaves']]
    
    orderedVal = df
    
    if cluster_rows:
        distances = scipy.cluster.hierarchy.distance.pdist(df.values)
        rowY = scipy.cluster.hierarchy.linkage(distances)
        rowZ = scipy.cluster.hierarchy.dendrogram(rowY, orientation='right', no_plot=True)
        orderedVal = df.reindex(index=df.axes[0][rowZ['leaves']])

        
    if cluster_columns:
        coldist = scipy.cluster.hierarchy.distance.pdist(df.values.transpose())
        cY = scipy.cluster.hierarchy.linkage(coldist)
        cZ = scipy.cluster.hierarchy.dendrogram(cY, no_plot=True)    
        orderedVal = orderedVal(columns=df.axes[1][cZ['leaves']])
    
    # row labels 
    pylab.yticks(range(0, len(orderedVal.index)), orderedVal.index)
    pylab.xticks(range(0, len(orderedVal.columns)), orderedVal.columns, rotation=90)

    #orderedVal = orderedVal[:,]
    pylab.tick_params(direction="out")
    pylab.imshow(orderedVal, interpolation="nearest", cmap=cm, norm=None)
    pylab.colorbar(shrink=0.4)
    #hcluster.dendrogram(Y, orientation='top')