#An undirected graph and a MCS sequence are passed into the networkX library to obtain local decomposition
import networkx as nx
from .Convex_hull_UG import * 


class LPD:

    def __init__(self, input_tuple):

        self.graph = input_tuple[0]
        self.mcs = input_tuple[1]

    def Decom_CMSA(self):
        block = []
        G_list = []
        G_list.append((self.graph, self.mcs[0]))
        while G_list:
            g, v = G_list.pop(0)  
            N_v = (set(g[v])|{v})
            if len(N_v)*(len(N_v)-1)/2 == len(nx.subgraph(g, N_v).edges):
                H = N_v
            else:
                H =  Convex_hull_UG(g).CMSA(N_v)
            block.append(H)
            for M in list(nx.connected_components(nx.subgraph(g, set(g.nodes)-H))):
                A = {n for n in nx.node_boundary(g, nbunch1=M, nbunch2=N_v)}|set(M)        
                G_list.append((nx.subgraph(g, A), min(A, key=lambda x: self.mcs.index(x))))
        return block
    
    def Decom_IPA(self):
        block = []
        G_list = []
        G_list.append((self.graph, self.mcs[0]))
        while G_list:
            g, v = G_list.pop(0)  
            N_v = (set(g[v])|{v})
            if len(N_v)*(len(N_v)-1)/2 == len(nx.subgraph(g, N_v).edges):
                H = N_v
            else:
                H =  Convex_hull_UG(g).IPA(N_v)
            block.append(H)
            for M in list(nx.connected_components(nx.subgraph(g, set(g.nodes)-H))):
                A = {n for n in nx.node_boundary(g, nbunch1=M, nbunch2=N_v)}|set(M)        
                G_list.append((nx.subgraph(g, A), min(A, key=lambda x: self.mcs.index(x))))
        return block
    
#LPD_UG((G, mcs_sequence)).Local_decom_CMSA()
#LPD_UG((G, mcs_sequence)).Local_decom_IPA()