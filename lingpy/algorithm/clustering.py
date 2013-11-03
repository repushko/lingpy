# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2013-10-07 14:05
# modified : 2013-10-24 15:17
"""
Module provides general clustering functions for LingPy.
"""

__author__="Johann-Mattis List"
__date__="2013-10-24"

import codecs

try:
    from .cython import cluster as cluster
    from .cython import misc as misc
except ImportError:
    from .cython import _cluster as cluster
    from .cython import _misc as misc

from ..thirdparty import linkcomm as lc
from ..thirdparty import cogent as cg

from ..settings import rcParams

# thirdparty modules
import numpy as np

try:
    import networkx as nx
except ImportError:
    if rcParams['verbose']: print(rcParams['W_missing_module'].format('networkx'))

def flat_upgma(threshold,matrix,taxa=None,revert=False):
    """
    Carry out a flat cluster analysis based on the UPGMA algorithm \
    (:evobib:`Sokal1958`).
    
    Parameters
    ----------
 
    threshold : float
        The threshold which terminates the algorithm.   
    
    matrix : list or :py:class:`numpy.array`
        A two-dimensional list containing the distances.

    taxa : list (default = [])
        A list containing the names of the taxa. If the list is left empty, the
        indices of the taxa will be returned instead of their names.
    
    Returns
    -------
    
    clusters : dict
        A dictionary with cluster-IDs as keys and a list of the taxa
        corresponding to the respective ID as values.

    Examples
    --------
    The function is automatically imported along with LingPy.

    >>> from lingpy import *
    
    Create a list of arbitrary taxa.

    >>> taxa = ['German','Swedish','Icelandic','English','Dutch']
    
    Create an arbitrary distance matrix.

    >>> matrix = squareform([0.5,0.67,0.8,0.2,0.4,0.7,0.6,0.8,0.8,0.3])
    >>> matrix
    [[0.0, 0.5, 0.67, 0.8, 0.2],
     [0.5, 0.0, 0.4, 0.7, 0.6],
     [0.67, 0.4, 0.0, 0.8, 0.8],
     [0.8, 0.7, 0.8, 0.0, 0.3],
     [0.2, 0.6, 0.8, 0.3, 0.0]]

    Carry out the flat cluster analysis.

    >>> flat_upgma(0.6,matrix,taxa)
    {0: ['German', 'Dutch', 'English'], 1: ['Swedish', 'Icelandic']}

    See also
    --------
    ~lingpy.algorithm.clustering.flat_cluster
    ~lingpy.algorithm.clustering.flat_upgma
    ~lingpy.algorithm.clustering.fuzzy
    ~lingpy.algorithm.clustering.link_clustering
    ~lingpy.algorithm.clustering.mcl

    """
    if taxa is None:
        taxa = []

    return cluster.flat_upgma(threshold,matrix,taxa,revert)

def flat_cluster(
        method,
        threshold,
        matrix,
        taxa=None,
        revert=False
        ):
    """
    Carry out a flat cluster analysis based on linkage algorithms.
    
    Parameters
    ----------
    method : str { 'upgma', 'single', 'complete' }
        Select between 'ugpma', 'single', and 'complete'.
 
    threshold : float
        The threshold which terminates the algorithm.   
    
    matrix : list or :py:class:`numpy.array`
        A two-dimensional list containing the distances.

    taxa : list (default = [])
        A list containing the names of the taxa. If the list is left empty, the
        indices of the taxa will be returned instead of their names.
    
    Returns
    -------
    
    clusters : dict
        A dictionary with cluster-IDs as keys and a list of the taxa
        corresponding to the respective ID as values.

    Examples
    --------
    The function is automatically imported along with LingPy.

    >>> from lingpy import *
    
    Create a list of arbitrary taxa.

    >>> taxa = ['German','Swedish','Icelandic','English','Dutch']
    
    Create an arbitrary distance matrix.

    >>> matrix = squareform([0.5,0.67,0.8,0.2,0.4,0.7,0.6,0.8,0.8,0.3])
    >>> matrix
    [[0.0, 0.5, 0.67, 0.8, 0.2],
     [0.5, 0.0, 0.4, 0.7, 0.6],
     [0.67, 0.4, 0.0, 0.8, 0.8],
     [0.8, 0.7, 0.8, 0.0, 0.3],
     [0.2, 0.6, 0.8, 0.3, 0.0]]

    Carry out the flat cluster analysis.

    >>> flat_cluster('upgma',0.6,matrix,taxa)
    {0: ['German', 'Dutch', 'English'], 1: ['Swedish', 'Icelandic']}

    See also
    --------
    ~lingpy.algorithm.clustering.flat_cluster
    ~lingpy.algorithm.clustering.flat_upgma
    ~lingpy.algorithm.clustering.fuzzy
    ~lingpy.algorithm.clustering.link_clustering
    ~lingpy.algorithm.clustering.mcl

    """
    if taxa is None:
        taxa = []

    return cluster.flat_cluster(method,threshold,matrix,taxa,revert)

def upgma(
        matrix,
        taxa,
        distances = True
        ):
    """
    Carry out a cluster analysis based on the UPGMA algorithm \
    (:evobib:`Sokal1958`).

    Parameters
    ----------

    matrix : list or :py:class:`numpy.array`
        A two-dimensional list containing the distances.

    taxa : list
        An list containing the names of all taxa corresponding to the distances
        in the matrix.

    distances : bool
        If set to ``False``, only the topology of the tree will be returned.

    Returns
    -------

    newick : str
        A string in newick-format which can be further used in biological
        software packages to view and plot the tree.

    Examples
    --------
    Function is automatically imported when importing lingpy.

    >>> from lingpy import *
    
    Create an arbitrary list of taxa.

    >>> taxa = ['German','Swedish','Icelandic','English','Dutch']
    
    Create an arbitrary matrix.

    >>> matrix = squareform([0.5,0.67,0.8,0.2,0.4,0.7,0.6,0.8,0.8,0.3])

    Carry out the cluster analysis.

    >>> upgma(matrix,taxa,distances=False)
    '((Swedish,Icelandic),(English,(German,Dutch)));'

    See also
    --------
    ~lingpy.algorithm.clustering.neighbor   
    """

    return cluster.upgma(matrix,taxa,distances)

def neighbor(matrix,taxa,distances=True):
    """
    Function clusters data according to the Neighbor-Joining algorithm \
    (:evobib:`Saitou1987`).
    
    Parameters
    ----------

    matrix : list or :py:class:`numpy.array`
        A two-dimensional list containing the distances.

    taxa : list
        An list containing the names of all taxa corresponding to the distances
        in the matrix.

    distances : bool
        If set to ``False``, only the topology of the tree will be returned.

    Returns
    -------

    newick : str
        A string in newick-format which can be further used in biological
        software packages to view and plot the tree.

    Examples
    --------
    Function is automatically imported when importing lingpy.

    >>> from lingpy import *
    
    Create an arbitrary list of taxa.

    >>> taxa = ['Norwegian','Swedish','Icelandic','Dutch','English']
    
    Create an arbitrary matrix.

    >>> matrix = squareform([0.5,0.67,0.8,0.2,0.4,0.7,0.6,0.8,0.8,0.3])

    Carry out the cluster analysis.

    >>> neighbor(matrix,taxa)
    '(((Norwegian,(Swedish,Icelandic)),English),Dutch);'

    See also
    --------
    ~lingpy.algorithm.cluster.upgma
    """
    
    return cluster.upgma(matrix,taxa,distances)

def fuzzy(threshold,matrix,taxa,method='upgma',revert=False):
    """
    Create fuzzy cluster of a given distance matrix.
    
    Parameters
    ----------
    threshold : float
        The threshold that shall be used for the basic clustering of the data.

    matrix : list or :py:class:`numpy.array`
        A two-dimensional list containing the distances.

    taxa : list
        An list containing the names of all taxa corresponding to the distances
        in the matrix.

    distances : bool
        If set to ``False``, only the topology of the tree will be returned.

    revert : bool (default=False)
        Specify whether a reverted dictionary should be returned. 
    
    Returns
    -------
    cluster : dict
        A dictionary with cluster-IDs as keys and a list as value, containing
        the taxa that are assigned to a given cluster-ID.

    Examples
    --------
    The function is automatically imported along with LingPy.

    >>> from lingpy import *
    
    Create a list of arbitrary taxa.

    >>> taxa = ['German','Swedish','Icelandic','English','Dutch']
    
    Create an arbitrary distance matrix.

    >>> matrix = squareform([0.5,0.67,0.8,0.2,0.4,0.7,0.6,0.8,0.8,0.3])
    >>> matrix
    [[0.0, 0.5, 0.67, 0.8, 0.2],
     [0.5, 0.0, 0.4, 0.7, 0.6],
     [0.67, 0.4, 0.0, 0.8, 0.8],
     [0.8, 0.7, 0.8, 0.0, 0.3],
     [0.2, 0.6, 0.8, 0.3, 0.0]]

    Carry out the fuzzy flat cluster analysis.

    >>> fuzzy(0.5,matrix,taxa)
    {1: ['Swedish', 'Icelandic'], 2: ['Dutch', 'German'], 3: ['Dutch', 'English']}
    
    Notes
    -----
    This is a very simple fuzzy clustering algorithm. It basically does nothing
    else than removing taxa successively from the matrix, flat-clustering the
    remaining taxa with the corresponding threshold, and then returning a
    combined "consensus" cluster in which taxa may be assigned to multiple
    clusters.

    See also
    --------
    ~lingpy.algorithm.clustering.link_clustering
    """
    try:
        g = nx.Graph()
    except NameError:
        print(rcParams['W_missing_module'].format('networkx'))
        return

    for taxon in taxa: g.add_node(taxon)

    for idx,taxon in enumerate(taxa):    
    
        new_matrix = []
        for i,line in enumerate(matrix):
            for j,cell in enumerate(line):
                if i < j and i != idx and j != idx:
                    new_matrix += [cell]
        new_matrix = misc.squareform(new_matrix)
        
        clusters = cluster.flat_cluster(
                method,
                threshold,
                new_matrix,
                [t for t in taxa if t != taxon]
                )

        if rcParams['verbose']: print(taxon,idx,clusters)

        for clr in clusters:
            for i,tA in enumerate(clusters[clr]):
                for j,tB in enumerate(clusters[clr]):
                    if i < j:
                        try:
                            g.edge[tA][tB]['weight'] += 1
                        except:
                            g.add_edge(tA,tB,weight=1)
    i = 1
    out = {}
    for c in nx.find_cliques(g):
        out[i] = c
        i += 1

    if revert:
        new_out = {}
        for key,val in out.items():
            for v in val:
                try:
                    new_out[v] += [key]
                except KeyError:
                    new_out[v] = [key]
        return new_out

    return out

def matrix2tree(
        matrix,
        taxa,
        tree_calc = "neighbor",
        distances = True,
        filename = ''
        ):
    """
    Calculate a tree of a given distance matrix.

    Parameters
    ----------
    matrix : {list, numpy.array}
        The distance matrix to be used.
    taxa : list
        A list of the taxa in the distance matrix.
    tree_calc : str (default='neighbor')
        The method for tree calculation that shall be used. Select between:

        * 'neighbor': Neighbor-joining method (:evobib:`Saitou1987`)
        * 'upgma' : UPGMA method (:evobib:`Sokal1958`)
    distances : bool (default=True)
        If set to c{True}, distances will be included in the
        tree-representation.
    filename : str (default='')
        If a filename is specified, the data will be written to that file.

    Returns
    -------
    tree : ~lingpy.thirdparty.cogent.tree.PhyloNode
        A ~lingpy.thirdparty.cogent.tree.PhyloNode object for handling tree
        files.
    """
    
    if tree_calc == 'upgma':
        algorithm = cluster.upgma
    elif tree_calc == 'neighbor':
        algorithm = cluster.neighbor

    newick = algorithm(matrix,taxa,distances)

    tree = cg.LoadTree(treestring=newick)
    
    if not filename:
        return tree
    else:
        out = codecs.open(filename+'.nwk','w','utf-8')
        out.write(str(tree))
        out.close()
        if rcParams['verbose']: print(rcParams['M_file_written'].format(filename,'nwk'))
    
def matrix2groups(
        threshold,
        matrix,
        taxa,
        cluster_method = 'upgma'
        ):
    """
    Calculate flat cluster of distance matrix.

    Parameters
    ----------
    threshold : float
        The threshold to be used for the calculation.
    matrix : {list, numpy.array}
        The distance matrix to be used.
    taxa : list
        A list of the taxa in the distance matrix.

    Returns
    -------
    groups : dict
        A dictionary with the taxa as keys and the group assignment as values.

    Notes
    -----
    This function is important for internal calculations within wordlist. It is
    not recommended for further use.
    """
    
    if cluster_method not in ['mcl','markov']:
        flats = cluster.flat_cluster(
                cluster_method,
                threshold,
                matrix,
                taxa = [t for t in taxa],
                )
    elif cluster_method in ['mcl','markov']:
        flats = mcl(
                threshold,
                matrix,
                taxa
                )
    
    mapper = dict(zip(flats,range(1,len(taxa)+1)))
    out = {}
    for i,key in enumerate(flats):
        n = 'G_{0}'.format(mapper[key])
        if cluster_method not in ['mcl','markov']:
            for t in flats[key]:
                out[t] = n
        else:
            out[taxa[i]] = n
    return out
        

    groups = [flats[i] for i in range(len(taxa))]
    
    # renumber the groups
    groupset = sorted(set(groups))
    renum = dict([(i,j+1) for i,j in zip(
        groupset,
        range(len(groupset))
        )])
    groups = [renum[i] for i in groups]

    return dict(zip(taxa,['G_{0}'.format(g) for g in groups]))

def _get_wad(matrix, threshold, use_log=False):
    """
    Get weighted average degree.
    """
    if use_log:
        log_f = lambda x: -np.log(1-x)
    else:
        log_f = lambda x: x

    degreeDict = {}

    for i in range(len(matrix)):
        for j in range(i+1,len(matrix)):
            score = matrix[i][j]
            if score < threshold:
                deg = log_f(score)
                try:
                    degreeDict[i] += [deg]
                except KeyError:
                    degreeDict[i] = [deg]
                try:
                    degreeDict[j] += [deg]
                except KeyError:
                    degreeDict[j] = [deg]
    
    deg_sum = 0
    for weights in degreeDict.values():
        deg = sum(weights)
        deg_sum += deg

    if degreeDict:
        return deg_sum / len(degreeDict)

def find_threshold(
        matrix,
        thresholds=[i*0.05 for i in range(1,19)][::-1],
        logs = True
        ):
    """
    Use a variant of the method by :evobib:`Apeltsin2011` in order to find an optimal threshold.

    Parameters
    ----------
    matrix : list
        The distance matrix for which the threshold shall be determined.
    thresholds : list (default = [i*0.05 for i in range(1,19)[::-1])
        The range of thresholds that shall be tested.
    logs : {bool,builtins.function} (default=True)
        If set to c{True}, the logarithm of the score beyond the threshold will
        be assigned as weight to the graph. If set to c{False} all weights will
        be set to 1. Use a custom function to define individual ways to
        calculate the weights.

    Returns
    -------
    threshold : {float,None}
        If a float is returned, this is the threshold identified by the method.
        If c{None} is returned, no threshold could be identified.

    Notes
    -----
    This is a very simple method that may not work well depending on the
    dataset. So we recommend to use it with great care.
    """
 
    # get the old degree of the matrix
    odeg = _get_wad(matrix,1)
    
    # store the plateaus (where nothing changes in the network)
    plato = {0:[1.0]}
    
    # this is the current index of the last plateau
    ci = 0
    minc = 0
    mint = 1.0
    
    alls = []

    # start iterating and calculating
    for i,t in enumerate(thresholds[1:],1):
        
        # get the new degree of the matrix under threshold t
        ndeg = _get_wad(matrix,t,logs)
        
        # if there is a new degree
        if ndeg:

            # get the change in comparison with the old degree
            cdeg = ndeg - odeg

            if cdeg < minc:
                minc = cdeg
                mint = t
            
            # swap old degree to new degree
            odeg = ndeg

            # if there's a plateau, the changed degree should be equal or
            # greater zero
            if cdeg >= 0:
                plato[ci] += [t]
            else:
                plato[i] = [t]
                ci = i

            alls += [(t,ndeg)]

    # try to find the plateau of maximal length
    sorted_plato = sorted(
            plato,
            key = lambda x: len(plato[x]),
            reverse = True
            )
    #return [mint] 
    if rcParams['verbose']: 
        print('[i] Found {0} thresholds.'.format(
            len([p for p in plato if len(plato[p]) > 1])))
        print('... ',sorted([len(plato[p]) for p in plato],reverse=True))
    # check if first entry is NOT of length 1
    try:
        return [sum(plato[t]) / len(plato[t]) for t in sorted_plato if len(plato[t]) > 1][0]
    except:
        return
        # get the median
        results = [r[1] for r in alls]
        if len(results) / 2 != len(results) // 2:
            median = sorted(results)[(len(results)-1)//2]
            return alls[results.index(median)][0]
        else:
            if results:
                median1 = sorted(results)[(len(results)-1)//2]
                median2 = sorted(results)[len(results)//2]
                r1 = alls[results.index(median1)][0]
                r2 = alls[results.index(median2)][0]
                return r1+r2 / 2
        return
       
    
    #if len(plato[sorted_plato[0]]) > 1 and sorted_plato[0] != 0:
    #    t = plato[sorted_plato[0]][-1]
    #    return t
    #elif len(plato[sorted_plato[0]]) > 1:
    #    if len(sorted_plato) > 1:
    #        if len(plato[sorted_plato[1]]) > 1:
    #            return plato[sorted_plato[1]][-1]
    #        else:
    #            return plato[sorted_plato[0]][-1]
    #    else:
    #        return plato[sorted_plato[0]][-1]
    #elif len(plato[sorted_plato[0]]) > 1:
    #    return plato[sorted_plato[0]][-1]
            

def link_clustering(
        threshold,
        matrix,
        taxa,
        link_threshold=False,
        revert=False,
        matrix_type = 'distances',
        fuzzy = True
        ):
    """
    Carry out a link clustering analysis using the method by :evobib:`Ahn2010`.

    Parameters
    ----------
    threshold : {float, bool}
        The threshold that shall be used for the initial selection of links
        assigned to the data. If set to c{False}, the weights from the matrix
        will be used directly.

    matrix : list or :py:class:`numpy.array`
        A two-dimensional list containing the distances.

    taxa : list
        An list containing the names of all taxa corresponding to the distances
        in the matrix.

    link_threshold : float (default=0.5)
        The threshold that shall be used for the internal clustering of the
        data.

    matrix_type : {"distances","similarities","weights"} (default="distances")
        Specify the type of the matrix. If the matrix contains distance data,
        it will be adapted to similarity data. If it contains "similarities",
        no adaptation is needed. If it contains "weights", a weighted version
        of link clustering (see the supplementary in :evobib:`Ahn2010` for
        details) ]will be carried out.

    Returns
    -------
    cluster : dict
        A dictionary with cluster-IDs as keys and a list as value, containing
        the taxa that are assigned to a given cluster-ID.

    Examples
    --------

    The function is automatically imported along with LingPy.

    >>> from lingpy import *
    
    Create a list of arbitrary taxa.

    >>> taxa = ['German','Swedish','Icelandic','English','Dutch']
    
    Create an arbitrary distance matrix.

    >>> matrix = squareform([0.5,0.67,0.8,0.2,0.4,0.7,0.6,0.8,0.8,0.3])
    >>> matrix
    [[0.0, 0.5, 0.67, 0.8, 0.2],
     [0.5, 0.0, 0.4, 0.7, 0.6],
     [0.67, 0.4, 0.0, 0.8, 0.8],
     [0.8, 0.7, 0.8, 0.0, 0.3],
     [0.2, 0.6, 0.8, 0.3, 0.0]]

    Carry out the link-clustering analysis.

    >>> link_clustering(0.5,matrix,taxa)
    {1: ['Dutch', 'English', 'German'], 2: ['Icelandic', 'Swedish']}

    See also
    --------
    ~lingpy.algorithm.clustering.fuzzy
    """
    # check for matrix type
    if matrix_type == 'distances':
        evaluate = lambda x:True if x < threshold else False
    elif matrix_type == 'similarities':
        evaluate = lambda x:True if x > threshold else False
    elif matrix_type == 'weights':
        evaluate = lambda x:False

    # get the edges and the adjacency from the thresholds
    edges = set()
    adjacency = dict([(t,set()) for t in taxa])
    weights = {}

    for i,taxA in enumerate(taxa):
        for j,taxB in enumerate(taxa):
            if i < j:
                if evaluate(matrix[i][j]):
                    edges.add((taxA,taxB))
                    adjacency[taxA].add(taxB)
                    adjacency[taxB].add(taxA)
                elif matrix_type == 'weights':
                    if matrix[i][j] < threshold:
                        edges.add((taxA,taxB))
                        adjacency[taxA].add(taxB)
                        adjacency[taxB].add(taxA)
                        edges.add((taxB,taxA))
                        weights[taxA,taxB] = -np.log2((1-matrix[i][j])**2)
                    
    if not weights:
        weights = None
    
    if edges:
        # initialize the HLC object
        hlc = lc.HLC(adjacency,edges)
    else:
        # check for null edges: if they occur, return the clusters directly
        if revert:
            if fuzzy:
                return dict([(a,[b]) for a,b in zip(taxa,range(len(taxa)))])
            else:
                return dict([(a,b) for a,b in zip(taxa,range(len(taxa)))])
        else:
            if fuzzy:
                return dict([(a,[b]) for a,b in zip(range(len(taxa)),taxa)])
            else:
                return dict([(a,b) for a,b in zip(range(len(taxa)),taxa)])

    # carry out the analyses using defaults for the clustering
    comms = hlc.single_linkage(threshold=link_threshold,w=weights)
    edge2cid = comms[0]
    
    # retrieve all clusterings for the nodes
    cluster = dict([(t,[]) for t in taxa])
    
    # retrieve the data
    clr2nodes = dict()
    clr2edges = dict()
    
    # count the links of 
    for edge,idx in edge2cid.items():
        nodeA,nodeB = edge[0],edge[1]

        try:
            clr2edges[idx] += [edge]
        except KeyError:
            clr2edges[idx] = [edge]
        try:
            clr2nodes[idx] += [nodeA,nodeB]
        except KeyError:
            clr2nodes[idx] = [nodeA,nodeB]

    for idx in clr2nodes:
        clr2nodes[idx] = sorted(set(clr2nodes[idx]))
    
    # delete all clusters that appear as subsets of larger clusters
    delis = []
    for keyA in sorted(clr2nodes):
        for keyB in sorted(clr2nodes):
            if keyA != keyB:
                valsA = set(clr2nodes[keyA])
                valsB = set(clr2nodes[keyB])
                
                if valsA != valsB:
                    if valsA.issubset(valsB):
                        delis += [keyA]
                    elif valsB.issubset(valsA):
                        delis += [keyB]
                elif valsA == valsB:
                    delis += [keyB]
    for k in set(delis):
        del clr2nodes[k]

    # renumber the data
    mapper = dict(zip(clr2nodes.keys(),range(1,len(clr2nodes)+1)))
    
    out = {}
    found = []
    for idx in clr2nodes:
        out[mapper[idx]] = clr2nodes[idx]
        found += clr2nodes[idx]
    missing = [f for f in taxa if f not in found]
    idx = max(out.keys())+1
    for m in missing:
        out[idx] = [m]
        idx += 1
    
    # determine weights for communities to edges
    node_weights = dict([(t,{}) for t in taxa])
    for c,e in clr2edges.items():
        for nA,nB in e:
            if c in mapper:
                this_c = mapper[c]
                try:
                    node_weights[nA][this_c] += 1
                except KeyError:
                    node_weights[nA][this_c] = 1
                try:
                    node_weights[nB][this_c] += 1
                except KeyError:
                    node_weights[nB][this_c] = 1

    # revert stuff first
    cluster = dict([(t,[]) for t in taxa])
    for idx in out:
        for t in out[idx]:
            cluster[t] += [idx]
    
    # weight membership of nodes and assign to most prominent community
    if not fuzzy:
        new_cluster = {}
        for t,clr in cluster.items():
            weighted = sorted(
                    clr,
                    key = lambda x: node_weights[t][x] if x in node_weights[t] else 0,
                    reverse=True
                    )
            new_cluster[t] = weighted[0]
        if revert:
            return dict([(taxa.index(t),c) for t,c in new_cluster.items()])    
        else:
            out = dict([(c,[]) for c in set(new_cluster.values())])
            for t,c in new_cluster.items():
                out[c] += [t]
        return out
            
    if not revert:
        return out
    else:
        cluster = dict([(t,[]) for t in taxa])
        for idx in out:
            for t in out[idx]:
                cluster[t] += [idx]

        return cluster

# the following lines of code are devoted to mcl clustering algorithm

def _normalize_matrix(matrix):
    """
    Normalize the matrix.
    """
    return matrix / sum(matrix)

def _is_idempotent(matrix):
    """
    Check whether the matrix is idempotent.
    """

    for line in matrix:
        if len([x for x in set(line) if x != 0]) > 1:
            return False
    return True

def _interprete_matrix(
        matrix
        ):
    """
    Look for attracting nodes in the matrix.
    """
    if rcParams['debug']: print(matrix)

    clusters = []
    flags = len(matrix) * [False]
    for i in range(len(matrix)):
        clr = []
        for j in range(len(matrix)):
            if not flags[j] and matrix[i][j] > 0:
                clr += [j]
                flags[j] = True
        if clr:
            clusters += [clr]
    
    # make a converter for length
    out = [0 for i in range(len(matrix))]
    idx = 1 
    for clr in clusters:
        for i in clr:
            out[i] = idx
        idx += 1

    if sum(out) == 0:
        return list(range(len(out)))
    
    return out

def mcl(
        threshold,
        matrix,
        taxa,
        max_steps = 1000,
        inflation = 2,
        expansion = 2,
        add_self_loops = True,
        revert = False,
        logs = True,
        matrix_type = "distances"
        ):
    """
    Carry out a clustering using the MCL algorithm (:evobib:`Dongen2000`).

    Parameters
    ----------
    threshold : {float, bool}
        The threshold that shall be used for the initial selection of links
        assigned to the data. If set to c{False}, the weights from the matrix
        will be used directly.

    matrix : list or :py:class:`numpy.array`
        A two-dimensional list containing the distances.

    taxa : list
        An list containing the names of all taxa corresponding to the distances
        in the matrix.

    max_steps : int (default=1000)
        Maximal number of iterations.

    inflation : int (default=2)
        Inflation parameter for the MCL algorithm.

    expansion : int (default=2)
        Expansion parameter of the MCL algorithm.

    add_self_loops : {True, False, builtins.function} (default=True)
        Determine whether self-loops should be added, and if so, how they
        should be weighted. If a function for the calculation of self-loops is
        given, it will take the whole column of the matrix for each taxon as
        input.
    
    logs : {bool,builtins.function} (default=True)
        If set to c{True}, the logarithm of the score beyond the threshold will
        be assigned as weight to the graph. If set to c{False} all weights will
        be set to 1. Use a custom function to define individual ways to
        calculate the weights.
    
    matrix_type : {"distances", "similarities"}
        Specify the type of the matrix. If the matrix contains distance data,
        it will be adapted to similarity data. If it contains "similarities",
        no adaptation is needed.
    
    Examples
    --------

    The function is automatically imported along with LingPy.

    >>> from lingpy import *
    
    Create a list of arbitrary taxa.

    >>> taxa = ['German','Swedish','Icelandic','English','Dutch']
    
    Create an arbitrary distance matrix.

    >>> matrix = squareform([0.5,0.67,0.8,0.2,0.4,0.7,0.6,0.8,0.8,0.3])
    >>> matrix
    [[0.0, 0.5, 0.67, 0.8, 0.2],
     [0.5, 0.0, 0.4, 0.7, 0.6],
     [0.67, 0.4, 0.0, 0.8, 0.8],
     [0.8, 0.7, 0.8, 0.0, 0.3],
     [0.2, 0.6, 0.8, 0.3, 0.0]]

    Carry out the link-clustering analysis.

    >>> mcl(0.5,matrix,taxa)
    {1: ['German', 'English', 'Dutch'], 2: ['Swedish', 'Icelandic']}

    """
    # check for type of matrix
    if type(matrix) != np.ndarray:
        imatrix = np.array(matrix)
    else:
        imatrix = matrix.copy()
    
    # check for matrix type and decide how to handle logs
    if matrix_type == 'distances':
        evaluate = lambda x: True if x < threshold else False
        if logs == True:
            logs = lambda x: -np.log2((1-x)**2)
        elif logs == False:
            logs = lambda x: x
    elif matrix_type == 'similarities':
        evaluate = lambda x: True if x > threshold else False
        if logs == True:
            logs = lambda x: -np.log(x**2)
        else:
            logs = lambda x: x

    # check for threshold
    if threshold:
        
        for i in range(len(imatrix)):
            for j in range(i+1,len(imatrix)):
                score = imatrix[i][j]
                if evaluate(score):
                    imatrix[i][j] = logs(score)
                    imatrix[j][i] = logs(score)
                else:
                    imatrix[i][j] = 0
                    imatrix[j][i] = 0
    
    # check for self_loops
    if add_self_loops == True:
        for i in range(len(imatrix)):
            imatrix[i][i] = 1
    elif add_self_loops == False:
        pass
    else:
        for i in range(len(imatrix)):
            imatrix[i][i] = add_self_loops(imatrix[:,i])

    if rcParams['debug']: print("[DEBUG]\n",imatrix)

    # normalize the matrix
    imatrix = _normalize_matrix(imatrix)

    # start looping and the like
    steps = 0
    while True:
        
        # expansion
        imatrix = np.linalg.matrix_power(imatrix,expansion)
        
        # inflation
        imatrix = imatrix ** inflation

        # normalization
        imatrix = _normalize_matrix(imatrix)

        # increase steps
        steps += 1

        # check for matrix convergence
        if steps >= max_steps or _is_idempotent(imatrix):
            if rcParams['debug']:
                print("[DEBUG] Number of steps {0}.".format(steps))
            break
    
    # retrieve the clusters
    clusters = _interprete_matrix(imatrix)

    # modify clusters
    if revert:
        return dict(
                zip(
                    range(len(taxa)),
                    clusters
                    )
                )
    
    clr = {}
    for i,t in enumerate(taxa):
        try:
            clr[clusters[i]] += [t]
        except:
            clr[clusters[i]] = [t]

    return clr

def partition_density(matrix,t):
    """
    Calculate partition density for a given threshold on a distance matrix.
    
    Notes
    -----
    See :evobib:`Ahn2012` for details on the calculation of partition density
    in a given network.
    """
    
    # compute cutoff for matrix at t
    m = np.zeros((len(matrix),len(matrix)))

    for i in range(len(matrix)):
        for j in range(i+1,len(matrix)):
            if matrix[i][j] < t:
                m[i][j] = 1
                m[j][i] = 1
    # get the total number of links
    T = sum(m.flatten()) / 2
    
    # get connected components
    nodes = list(range(len(m)))
    idx = 1
    parts = [0 for i in range(len(m))]
    
    for i in range(len(m)):
        for j in range(i+1,len(m)):
            if m[i][j] == 1:
                if parts[i] == parts[j] and parts[i] != 0:
                    pass
                else:
                    # most complicated, update all the stuff
                    if parts[i] > 0 and parts[j] > 0:
                        
                        # determine best idx
                        if parts[i] > parts[j]:
                            this = parts[j]
                            other = parts[i]
                        else:
                            this = parts[i]
                            other = parts[j]
                            
                        # find all neighbors of the 
                        idxs = [n for n in nodes if parts[n] == other]
                        for n in idxs:
                            parts[n] = this
                    elif parts[i] == 0 and parts[j] == 0:
                        parts[i] = idx
                        parts[j] = idx
                        idx += 1
                    elif parts[i] > 0:
                        parts[j] = parts[i]
                    elif parts[j] > 0:
                        parts[i] = parts[j]
    
    # finish unconnected components
    for i,p in enumerate(parts):
        if p == 0:
            parts[i] = max(parts) + 1

    # convert to dictionary
    components = sorted(set(parts))

    # return zero, if all components are different
    if len(components) == len(m):
        return 0.0,len(components)

    # count density
    D = 0

    for part in components:
        # get nodes
        nodes = [n for n in range(len(parts)) if parts[n] == part]

        # get edges
        edges = 0
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                if m[nodes[i]][nodes[j]] == 1:
                    edges += 1

        N = len(nodes)
        M = edges
        
        # calculate sum formula
        x = 1
        try:

            t = M * (M - (N - x)) / ((N - 1 + x) * ( N -x))
            D += t
        except ZeroDivisionError:
            pass

    return 2 / T * D,len(components)

def best_threshold(
        matrix,
        trange = (0.3,0.7,0.05)
        ):
    """
    Calculate the best threshold by maximizing partition density for a given range of thresholds.
    
    Notes
    -----
    This method makes use of the idea of partition density proposed in
    :evobib:`Ahn2010`.

    """
    best_score = 0
    best_t = False
    pds = []
    for t in np.arange(*trange):
        p = partition_density(matrix,t)
        pds += [(p[0],p[1],t)]

    # strip off the hightes values from the end
    delis = []
    pds = pds[::-1]
    start = pds[0][0]
    for i,(p1,p2,t) in enumerate(pds):
        if p1 == start:
            delis += [i]
        else:
            break
    
    if len(delis) == len(pds):
        return 0.5 * (trange[1] - trange[0])
    
    for d in delis[::-1]:
        del pds[d]

    pds = pds[::-1]
    delis = []
    start = pds[0][0]
    for i,(p1,p2,t) in enumerate(pds):
        if p1 == start:
            delis += [i]
        else:
            break

    if len(delis) == len(pds):
        return 0.5 * (trange[1] - trange[0])

    for d in delis[::-1]:
        del pds[d]

    for p in pds:
        
        v = p[0] / (len(matrix)+1 - p[1])
        if v >= best_score:
            best_score = v
            best_t = p[2]
        else:
            pass
    return best_t
    
    
        
