"""
GenGA: Genome Graph Analysis package
A GWCNA + Co-expression networks analysis tool for gene expression analysis

Created by B.Sc. Andrés Santiago Martínez Hernandez

Advisors: PhD Natasha Bloch and PhD Felipe Giraldo

Copyright 2024 Andres Santiago Martinez Hernandez

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from tqdm import tqdm
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from PIL import Image
import community
import seaborn as sns
from matplotlib.colors import ListedColormap
from networkx.drawing.nx_pydot import graphviz_layout

class SuperGraph:

  def norms(self,method):
    adj1, adj2 = self.pair
    if method == "euclidean":
      return np.sqrt(np.sum(([np.round((aij1 - aij2)**2,2) for a1, a2 in zip(np.tril(adj1.todense()), np.tril(adj2.todense())) for aij1, aij2 in zip(a1,a2)])))
    elif method == "manhattan":
      return np.sum(([np.abs((aij1 - aij2)) for a1, a2 in zip(np.tril(adj1.todense()), np.tril(adj2.todense())) for aij1, aij2 in zip(a1, a2)]))
    elif method == "canberra":
      return np.sum([ np.abs(aij1-aij2)/1 if aij1 == aij2 and aij1 == 0 and aij2==0 else (np.abs(aij1 - aij2)/(np.abs(aij1)+np.abs(aij2)))  for a1, a2 in zip(np.tril(adj1.todense()), np.tril(adj2.todense())) for aij1 , aij2 in zip(a1,a2)])
    elif method == "jaccard":  # Weighted Jaccard
      JA1A2 = np.array([(np.min([aij1,aij2]),np.max([aij1,aij2])) for a1, a2 in zip(np.tril(adj1.todense()),np.tril(adj2.todense())) for aij1, aij2 in zip(a1,a2)])
      return 1 - (np.sum(JA1A2[:,0])/np.sum(JA1A2[:,1])) if np.sum(JA1A2[:,1]) != 0 else 1
    elif method == "deltacon": # DeltaCon distance by the Matusita approach
      A1, A2 = adj1.todense(), adj2.todense()
      I = np.identity(A1[0].shape[0]) #step 1: calculate I, D and prepare A.
      D1, D2 = I.copy(), I.copy()
      D1 = D1*[d[1] for d in self.dpair[0]]
      D2 = D2 * [d[1] for d in self.dpair[1]]
      S1 = I + (self.ev**2 * D1) - (self.ev * A1) #step 2: S = I + e**2D - eA
      S2 = I + (self.ev**2 * D2) - (self.ev * A2)
      rED = np.sqrt(np.sum(([(sij1 - sij2)**2 for s1, s2 in zip(S1,S2) for sij1 , sij2 in zip(s1,s2)]))) #step 3: Matusita (S1,S2)
      return 1/(1+ rED) #step 4: return sim instead of rootED 1/(1+d)
    elif method == "cut":
        """
        The metric is defined as
        - E is the sum of weights for a subset S,T (the remaining edges)
        - when comparing to graphs, it can be considered S and Sc instead of S,T
          where S and Sc are created by a cut
        - Random S partitions are created, the cut with the most weights attached (E(S,Sc)) 
          is the value of the distance
        The problem:
        - This metric seems to work over connected networks, thus, the partition 
          gives sets on which weights are not existent (and I don't really know how 
          to create the partitions)
        The implementation:
        - I would simply select randomly a set of edges, its complement is Sc, the edges 
          between S and Sc are counted. If this is the correct implementation I'm glad
          if not please review it.
        """
        V = np.sum([self.opair[0].get_edge_data(u,v)["weight"] for u, v in self.opair[0].edges])
        V += np.sum([self.opair[1].get_edge_data(u,v)["weight"] for u, v in self.opair[1].edges])
        random_vals = np.random.randint(1,len(self.opair[0].nodes()),5)
        cutsets_1 = [(list(self.opair[0].nodes)[:x],list(self.opair[0].nodes)[x:]) for x in random_vals]
        cutsets_2 = [(list(self.opair[1].nodes)[:x], list(self.opair[1].nodes)[x:]) for x in random_vals]
        """cutsets_1 = [(["A","B","C"],["D","E"]),
                     (["A", "B", "C","D"], ["E"]),
                     (["A", "E"], ["B","C","D"]),
                     (["D", "E", "C"], ["A", "B"]),
                     ]
        cutsets_2 = [(["A", "B", "C"], ["D", "E"]),
                     (["A", "B", "C", "D"], ["E"]),
                     (["A", "E"], ["B", "C", "D"]),
                     (["D", "E", "C"], ["A", "B"]),
                     ]
        """
        max_E = 0
        for c1, c2 in zip(cutsets_1,cutsets_2):
          E1 = np.sum([self.opair[0].get_edge_data(u,v)["weight"] if self.opair[0].get_edge_data(u,v) is not None else 0 for u in c1[0] for v in c1[1]])
          E2 = np.sum([self.opair[1].get_edge_data(u,v)["weight"] if self.opair[1].get_edge_data(u,v) is not None else 0 for u in c2[0] for v in c2[1]])
          E = 1/(V) * np.abs(E1 - E2)
          if E > max_E:
            max_E = E
        return max_E

  def __init__(self,name, graph_collection, method, e_val=0, normalize=False):
    self.name = name
    self.collection = graph_collection
    self.method = method
    self.graph = None
    self.graphic = None
    self.pair = None
    self.dpair = None
    self.opair = None
    self.ev = e_val
    self.construct_network(normalize)

  def __str__(self):
    return f"{self.name} supergraph network"

  def __repr__(self):
    return f"{self.name} supergraph network"

  def construct_network(self, normalize=False):
    print([(list(g.graph.nodes)) for g in self.collection])
    if np.unique([len(g.graph.nodes()) for g in self.collection]).shape[0] != 1:
      raise Exception(f"Not all of the graphs have the same number of nodes, hence it does not follow the KNC criteria \n {np.unique([len(g.graph.nodes()) for g in self.collection])}")
    sg = nx.Graph()
    if self.method == "euclidean" or self.method == "manhattan" or self.method == "jaccard" or self.method == "canberra" or self.method == "deltacon" or self.method == "cut":
      for g1 in self.collection:
        for g2 in self.collection:
          if g1.name != g2.name: #entities are different
            print(f"merging {g1.name} and {g2.name}")
            self.pair = nx.adjacency_matrix(g1.graph),nx.adjacency_matrix(g2.graph)
            if self.method == "deltacon" or self.method == "cut":
              self.dpair = nx.degree(g1.graph), nx.degree(g2.graph)
              if self.method == "cut":
                self.opair = g1.graph, g2.graph
            e = self.norms(self.method)
            if (g1.name,g2.name) not in sg.edges():
              sg.add_edge(g1.name,g2.name,weight=e)
    else:
      raise Exception("Invalid method")
    self.graph = sg
    if normalize:
      max = np.max([self.graph.get_edge_data(u,v)["weight"] for u,v in self.graph.edges()])
      for u,v in self.graph.edges():
        nx.set_edge_attributes(self.graph, {(u,v): {"weight":self.graph.get_edge_data(u,v)["weight"]/max}})

  def modify_adyancency(self,normalize=False,transform=False,alpha=1):
    adma = nx.adjacency_matrix(self.graph).todense()
    if transform:
      adma = np.exp((-adma**2)*alpha)
    if normalize:
      adma = adma/np.sum(np.tril(adma))
    return adma

  def create_network_union(self):
    try:
      if np.unique([len(g.nodes()) for g in self.collection]).shape[0] != 1:
        raise Exception("Not all of the graphs have the same number of nodes")
      graphs = self.collection
      self.graph = self.collection[0]
      graphs = graphs[1:]
      if self.method == "union":
        while len(graphs):
          self.graph = nx.union(self.graph, graphs[0], rename=("G1_","G2_"))
          graphs = graphs[1:]
      elif self.method == "intersection":
        while len(graphs):
          R = self.graph
          R.remove_nodes_from(n for n in self.graph if n not in graphs[0])
          R.remove_edges_from(e for e in self.graph.edges if e not in graphs[0].edges)
          self.graph = R
          graphs = graphs[1:]
      elif self.method == "special_union":
        while len(graphs):
          for e in graphs[0].edges:
            if e not in self.graph.edges:
              self.graph.add_edge(e[0],e[1], weight=graphs[0].get_edge_data(e[0],e[1])["weight"])
          graphs = graphs[1:]
      else:
        raise Exception("Invalid merging method")
    except Exception as e:
      print(f"Error, {e}")

  def get_degree(self, graphic=0):
    deg = sorted((d for n, d in self.graph.degree()), reverse=True)
    if graphic:
      fig, ax = plt.subplots()
      ax.plot(deg, "b-", marker="o")
      font = {"color": "k", "fontweight": "bold", "fontsize": 14}
      ax.set_title(f"{self.name} network degree", font)
      ax.set_ylabel("Degree")
      ax.set_xlabel("Rank")
      if graphic > 1:
        hfig, hax = plt.subplots()
        hax.bar(*np.unique(deg, return_counts=True))
        hax.set_title(f"{self.name} network histogram", font)
        hax.set_ylabel("# of nodes")
        hax.set_xlabel("degree")
        return hfig, fig, deg

      return fig, deg
    return deg
  def get_graphic(self):
    fig, ax = plt.subplots()
    cmap = plt.cm.RdYlGn
    pos = nx.shell_layout(self.graph)
    print([self.graph.get_edge_data(u,v) for u,v in self.graph.edges()])
    edge_c = [(self.graph.get_edge_data(u, v)["weight"]) for u, v in self.graph.edges()]
    edge_width = [(self.graph.get_edge_data(u, v)["weight"]) for u, v in self.graph.edges()] * 10
    nx.draw_networkx_nodes(self.graph, pos, node_color="gray", alpha=0.6)
    e = nx.draw_networkx_edges(self.graph, pos,
                               alpha=0.6,
                               edge_cmap=cmap,
                               edge_color=edge_c,
                               width=edge_width,
                               edge_vmin=-1,
                               edge_vmax=1)
    label_options = {"ec": "k", "fc": "white", "alpha": 0.2}
    nx.draw_networkx_labels(self.graph, pos, font_size=10, bbox=label_options, verticalalignment="bottom")
    font = {"color": "k", "fontweight": "bold", "fontsize": 14}
    ax.set_title(f"{self.name} Network", font)
    fig.colorbar(e, ax=ax)
    self.graphic = fig
    return self.graphic

  def get_distance_graph(self,adj_matrix,anatomic=False, zoom= 0.7, alpha_im=0,remove_self_edges=True, comms=None):

    df = pd.DataFrame(adj_matrix, columns=list(self.graph.nodes),index=list(self.graph.nodes))
    print(df)
    fig, ax = plt.subplots(figsize=(10,5))
    gauss_sg = nx.from_pandas_adjacency(df)
    if remove_self_edges:
      gauss_sg.remove_edges_from(list(nx.selfloop_edges(gauss_sg)))
    if anatomic:
      pos = {"ATN": (0.37, 0.45), "DI": (0.18, 0.48), "Dm": (0.25, 0.5),
             "Gc": (0.47, 0.49), "Hv": (0.3, 0.45), "POA": (0.3, 0.47),
             "TPp": (0.35, 0.46), "Vd": (0.21, 0.48), "Vs": (0.26, 0.49),
             "Vv": (0.21, 0.47)}
      i = Image.open("test_files\\guppyBrain_wf.png") #mimg.imread("test_files\\guppyBrain.png")
      i.putalpha(alpha_im)
      imbox = OffsetImage(i, zoom=zoom)
      ab = AnnotationBbox(imbox, (0.365, 0.48), frameon=False)
      ax.add_artist(ab)
    else:
      pos = nx.spring_layout(gauss_sg, seed=42)
    cmap = plt.colormaps.get_cmap("Blues")  #plt.cm.cool
    edge_c = [(gauss_sg.get_edge_data(u, v)["weight"]) for u, v in gauss_sg.edges()]
    edge_width = [(gauss_sg.get_edge_data(u, v)["weight"]) for u, v in gauss_sg.edges()] * 100
    if comms is not None:
      K = ["red", "blue", "green", "yellow", "purple","gray","black","pink"]
      n_colors = []
      for n in self.graph.nodes:
        for i,c in enumerate(comms):
          if n in c:
            n_colors.append(K[i])
      nx.draw_networkx_nodes(gauss_sg,pos,node_color=n_colors,alpha=0.6)
    else:
      nx.draw_networkx_nodes(gauss_sg, pos, node_color="gray", alpha=0.6)
    e = nx.draw_networkx_edges(gauss_sg, pos,
                               alpha=0.6,
                               edge_cmap=cmap,
                               edge_color=edge_c,
                               width=edge_width,
                               edge_vmin=np.min(adj_matrix),
                               edge_vmax=np.max(adj_matrix))
    label_options = {"ec": "k", "fc": "white", "alpha": 0.4}
    nx.draw_networkx_labels(gauss_sg, pos, font_size=13, bbox=label_options, verticalalignment="bottom")
    font = {"color": "k", "fontweight": "bold", "fontsize": 20}
    if comms is None:
      ax.set_title(f"{self.name} Network", font)
    else:
      ax.set_title(f"{self.name} Network (K = {len(comms)})")
    fig.colorbar(e, ax=ax)
    return fig

  def louvain_partition(self):
    coms = community.best_partition(self.graph,weight="weight",resolution=1E-30,random_state=30) #0.25 SINGLE PARTITION
    pos = nx.spring_layout(self.graph,seed=42)
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(
      self.graph,
      pos,
      node_color=list(coms.values()),
      cmap= plt.cm.Set1,
      node_size=200
    )
    label_options = {"ec": "k", "fc": "white", "alpha": 0.2}
    nx.draw_networkx_labels(self.graph, pos, font_size=10, bbox=label_options, verticalalignment="bottom")
    nx.draw_networkx_edges(self.graph, pos, alpha=0.5)
    plt.title(f"{self.name} Network Louvain partitions")
    plt.axis("off")
    for node, com in coms.items():
      print(f"Node: {node} | Community: {com}")
    return fig

  def create_junction_tree(self, graph):
    fig, ax = plt.subplots()
    j = nx.junction_tree(graph)
    print(f"JUNCTION TREE \n {list(j)}")
    pos = graphviz_layout(j, prog="twopi")
    nx.draw(j,pos,node_size=20, alpha=0.5, node_color="blue", with_labels=True)
    plt.axis("equal")
    return fig

  def get_communities(self,centrality=False, loaded=None):
    def most_central_edge(G):
      cen = nx.edge_betweenness_centrality(G, weight="weight")
      return max(cen, key=cen.get)

    if centrality:
      communities = list(nx.community.girvan_newman(self.graph, most_valuable_edge=most_central_edge))
    else:
      communities = list(nx.community.girvan_newman(self.graph))

    # Modularity -> measures the strength of division of a network into modules
    modularity_df = pd.DataFrame(
      [
        [k + 1, nx.community.modularity(self.graph, communities[k])]
        for k in range(len(communities))
      ],
      columns=["k", "modularity"],
    )

    def create_community_node_colors(graph, communities):
      number_of_colors = len(communities)
      colors = ["#D4FCB1", "#CDC5FC", "#FFC2C4", "#F2D140", "#BCC6C8"][:number_of_colors]
      node_colors = []
      print(communities)
      for node in graph:
        current_community_index = 0
        for community in communities:
          if node in community:
            node_colors.append(colors[current_community_index])
            break
          current_community_index += 1
      return node_colors

    # function to plot graph with node colouring based on communities
    def visualize_communities(graph, communities, i):
      node_colors = create_community_node_colors(graph, communities)
      modularity = round(nx.community.modularity(graph, communities), 6)
      title = f"Community Visualization of {len(communities)} communities with modularity of {modularity}"
      pos = nx.spring_layout(graph, k=0.3, iterations=50, seed=2)
      plt.subplot(3, 1, i)
      plt.title(title)
      nx.draw(
        graph,
        pos=pos,
        node_size=1000,
        node_color=node_colors,
        with_labels=True,
        font_size=20,
        font_color="black",
      )
    fig , ax = plt.subplots(3, figsize=(15,20))
    for c in communities:
      print(len(c))
    if loaded is not None:
      if type(loaded) == "dict_valueiterator":
        nx.drawg
      visualize_communities(self.graph,loaded,1)
    else:
      visualize_communities(self.graph, communities[0], 1)
      visualize_communities(self.graph, communities[2], 2)

    # Plot change in modularity as the important edges are removed
    modularity_df.plot.bar(
      x="k",
      ax=ax[2],
      color="#F2D140",
      title="Modularity Trend for Girvan-Newman Community Detection",
    )
    return fig

  def edge_histogram(self,adj_matrix,f=1,annot=True,triangular=False):
    fig, ax = plt.subplots()
    plt.title(f"Similarity matrix for {self.name} network")
    df = pd.DataFrame(adj_matrix, index=[i for i in self.graph.nodes], columns=[i for i in self.graph.nodes])
    if triangular:
      mask_upper = np.tril(np.ones_like(df, dtype=bool))  # Mask for upper triangle
      mask_lower = np.triu(np.ones_like(df, dtype=bool))
      dfm = df * mask_lower
      with sns.axes_style('white'):
        sns.heatmap(dfm, annot=True, cmap=ListedColormap(["white"]), cbar=False)
      for t in ax.texts:
        print(t.get_text())
        if t.get_text()=="0":
          t.set_text("")
        else:
          t.set_text(t.get_text())
      sns.heatmap(df, annot=False, mask=mask_lower, cbar=True, cmap="Blues")
    else:
      sns.heatmap(df, annot=annot, fmt=f".{f}f",cmap="Blues")
    return fig

  def community_methods(self,adj_matrix, method, k=4, seed=42, normalize=False,transform=False,a=1):
    df = pd.DataFrame(adj_matrix, columns=list(self.graph.nodes), index=list(self.graph.nodes))
    print(df)
    G = nx.from_pandas_adjacency(df)
    G.remove_edges_from(list(nx.selfloop_edges(G)))
    result = None
    print(f"Community creation Using {method} method")
    if method == "bisection":
      result = nx.community.kernighan_lin_bisection(G, weight="weight")
    elif method == "asynF":
      result = nx.community.asyn_fluidc(G,k=k, seed=seed)
    elif method == "fastlab":
      result = nx.community.fast_label_propagation_communities(G, weight="weight")
    elif method == "modularity":
      result = nx.community.greedy_modularity_communities(G, resolution=0.1, weight="weight",cutoff=k) #diferentes K y AIC u otro indicador de goodness of it
    elif method == "KQ":
      result = nx.community.k_clique_communities(G, k=k)
    print(list(result))
    return result
class Graph:
  def __init__(self,df,n,dir,corr_thr,corr_rule,imposed=False):
    self.name = n
    self.corr_mat = None
    self.dir = dir
    self.info = df
    self.conditions = corr_thr, corr_rule
    self.adj_mat = None
    self.graph = None
    self.graphic = None
    self.d_graph = None
    self.imposed = imposed
    if imposed:
      self.corr_mat = df
    self.calculate_adjacency_matrix()


  def __str__(self):
    return f"Graph: {self.name}"

  def __repr__(self):
    return f"GenGA graph {self.name}"

  def calculate_adjacency_matrix(self):
    if not self.imposed:
      self.corr_mat = self.info.corr(method="pearson").fillna(0)
    if self.conditions[1] == "sWGCNA":
      m = 0.5 + (0.5 * (self.corr_mat))
      self.adj_mat = m * (m >= self.conditions[0])
    elif self.conditions[1] == "standard" or self.imposed:
      corr_p , corr_n = (self.corr_mat * (self.corr_mat >= self.conditions[0])
                         , self.corr_mat * (self.corr_mat <= -self.conditions[0]))
      self.corr_mat = corr_p + corr_n
      self.adj_mat = self.corr_mat
    self.graph = nx.from_pandas_adjacency(self.adj_mat)
    self.graph.remove_edges_from(nx.selfloop_edges(self.graph))
  def get_centrality(self,type="default",graphics=0):

    cen = nx.degree_centrality(self.graph)
    if type == "eigenvector":
      cen = nx.eigenvector_centrality(self.graph)
    elif type == "katz":
      cen = nx.katz_centrality(self.graph)
    elif type == "pagerank":
      cen = nx.pagerank(self.graph)
    if graphics:
      fig, ax = plt.subplots()
    return cen

  def get_degree(self,graphic=0):
    deg = sorted((d for n, d in self.graph.degree()), reverse=True)
    if graphic:
      fig, ax = plt.subplots()
      ax.plot(deg, "b-",marker="o")
      font = {"color": "k", "fontweight": "bold", "fontsize": 14}
      ax.set_title(f"{self.name} network degree",font)
      ax.set_ylabel("Degree")
      ax.set_xlabel("Rank")
      if graphic > 1:
        hfig, hax = plt.subplots()
        hax.bar(*np.unique(deg,return_counts=True))
        hax.set_title(f"{self.name} network histogram", font)
        hax.set_ylabel("# of nodes")
        hax.set_xlabel("degree")
        return hfig, fig, deg

      return fig, deg
    return deg

  def get_adjacency_matrix(self):
    return self.adj_mat

  def set_graph(self):
    self.graph = nx.from_pandas_adjacency(self.adj_mat)

  def get_graphic(self,overwrite=False):
    if self.graphic is None or overwrite:
      self.d_graph = nx.from_pandas_adjacency(self.corr_mat)
      self.d_graph.remove_edges_from(nx.selfloop_edges(self.d_graph))
      fig, ax = plt.subplots()
      cmap = plt.cm.RdYlGn
      colors = range(0,self.d_graph.number_of_edges())
      print(colors)
      pos = nx.shell_layout(self.d_graph)
      edge_c = [(self.d_graph.get_edge_data(u,v)["weight"])for u,v in self.d_graph.edges()]
      print(edge_c)
      edge_width = [(self.d_graph.get_edge_data(u,v)["weight"])for u,v in self.d_graph.edges()]*10
      nx.draw_networkx_nodes(self.d_graph,pos,node_color="gray",alpha=0.6)
      e = nx.draw_networkx_edges(self.d_graph, pos,
                             alpha=0.6,
                             edge_cmap=cmap,
                             edge_color=edge_c,
                             width=edge_width,
                             edge_vmin=-1,
                             edge_vmax=1)
      label_options = {"ec":"k","fc":"white","alpha":0.2}
      nx.draw_networkx_labels(self.d_graph,pos,font_size=10,bbox=label_options, verticalalignment="bottom")
      font = {"color": "k","fontweight": "bold", "fontsize": 14}
      ax.set_title(f"{self.name} Network",font)
      fig.colorbar(e, ax=ax)
      self.graphic = fig
      return self.graphic
    else:
      return self.graphic



def generate_genga_structure(dataframe, structure, nodes_info,save_route="",corr_thr=0.2,corr_rule="sWCGNA"):
  """
  Generates the genGA structure based on the dictionary structure and the uppermost value
  on the hierarchy.
  :param corr_rule: The rule for correlation treatment [sWGCNA, uWGCNA], default value is sWGCNA
  :param corr_thr: Correlation threshold, default value is 0.2 (20 percent)
  :param save_route: Optional, route to save the data on CSV, if "" information is not stored
  :param nodes_info: List containing [X_column, Y_column, Target_value]
  :param dataframe: Pandas DataFrame
  :param structure: Dictionary with the desired hierarchy.
  :return: A set of ordered Dataframes with the "leaf" Dataframes
  """
  conds, b_queries, f_queries = [], [], []
  dfs = []
  def calculate_structure(d, s):
    for k in d[s]:
      conds.append((s, k))
      nd = d[s][k]
      for sk in nd:
        if type(nd[sk]) is dict:
          calculate_structure(nd, sk)
        else:
          for le in nd[sk]:
            conds.append((sk, le))
            b_queries.append(conds.copy())
            conds.pop(-1)
        conds.pop(-1)
  def create_dfs(df,queries):
    df.fillna(0,inplace=True)
    for q in queries:
      d = ''.join(map(str,[f'{x[0]} == "{x[1]}" and ' if type(x[1]) is str else f'{x[0]} == {x[1]} and ' for x in q ]))
      f_queries.append(d[:-4])
      print(d[:-4])
      dfs.append(df.query(d[:-4]))

  def generate_wgcna_format(df,query,route):
    data = {}
    for i in range(len(df)):
      dat = df.iloc[i]
      if dat[nodes_info[0]] not in data:
        data[dat[nodes_info[0]]] = {dat[nodes_info[1]]: dat[nodes_info[2]]}
      else:
        data[dat[nodes_info[0]]][dat[nodes_info[1]]] = dat[nodes_info[2]]
    name = "".join(map(str,[f"{x[1]}_" for x in query]))[:-1]
    if route != "":
      pd.DataFrame.from_dict(data,orient="index").fillna(0).to_csv(f"{os.path.join(route,name)}.csv")
      print(f"Generated {os.path.join(route,name)}.csv")
    return pd.DataFrame.from_dict(data,orient="index").fillna(0)


  calculate_structure(structure,list(structure.keys())[0])
  print("Structure read")
  create_dfs(dataframe,b_queries)
  print("Dataframes created")
  graphs = []
  for d, q in tqdm(zip(dfs,b_queries)):
    n = "".join(map(str,[f"{x[1]}_" for x in q]))[:-1]
    g = Graph(generate_wgcna_format(d,q,save_route),n,save_route,corr_thr,corr_rule)
    g.graph.name = n.split("_")[-1].split(".")[0]
    graphs.append(g)

  return graphs


def load_df_from_xlsx(file,sheets=None):
  """
  Creates a dataframe or set of dataframes.
  :param file: Route to the file
  :param sheets: Iterable (list) of the sheet names
  :return: DF or dictionary of DFs based on sheet names
  """
  if sheets is not None:
    #Extract relevant sheets in DFs
    sol = {}
    for s in sheets:
      sol[s] = pd.read_excel(file, sheet_name=s)
    return sol
  else:
    return pd.read_excel(file)

def load_existing_adj_mtx(route,corr_thr=0.2,corr_rule="sWCGNA"):
  """
  Creates a GenGA Object from a WCGNA csv format
  :param route: path to csv file containing WCGNA structure
  :return: GenGA formated graph object
  """
  name, ext = route.split("\\")[-1].split(".")
  if ext == "csv":
    info = pd.read_csv(route, index_col=0)
  elif ext == "xlsx":
    info = pd.read_excel(route)
  g = Graph(info,name,route,corr_thr,corr_rule)
  return g
